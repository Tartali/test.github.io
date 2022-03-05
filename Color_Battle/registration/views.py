import uuid
import json

from django.core.paginator import Paginator
from rest_framework.views import APIView
from yookassa import Webhook
import var_dump as var_dump
from yookassa import Payment
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory

from yookassa import Configuration, Payment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.http import HttpResponseForbidden, HttpResponse
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from .models import Choose, Comment

from yookassa import Configuration, Payment
from yookassa.domain.common.user_agent import Version


def home(request):
    if request.user.is_authenticated:
        value = Choose.objects.all()
        somebody, created = Choose.objects.get_or_create(voter=request.user)
        sum_black = Choose.objects.aggregate(Sum('count_black'))
        sum_white = Choose.objects.aggregate(Sum('count_white'))
        sum_purple = Choose.objects.aggregate(Sum('count_purple'))

        sum_black_result = sum_black['count_black__sum']
        sum_white_result = sum_white['count_white__sum']
        sum_purple_result = sum_purple['count_purple__sum']

        all = sum_black['count_black__sum'] + sum_white['count_white__sum'] + sum_purple['count_purple__sum']
        percent_black = int(sum_black['count_black__sum'] * 100 / all)
        percent_white = int(sum_white['count_white__sum'] * 100 / all)
        percent_purple = int(sum_purple['count_purple__sum'] * 100 / all)

        context = {
            "value": value,
            "sum_black_result": sum_black_result,
            "sum_white_result": sum_white_result,
            "sum_purple_result": sum_purple_result,
            "percent_black": percent_black,
            "percent_white": percent_white,
            "percent_purple": percent_purple,
            "somebody": somebody
        }

        return render(request, 'registration/home.html', context)
    else:
        return render(request, 'registration/home.html')

def callback_payment(request):
    if request.method == 'POST':
        data = request.POST  # передаем в эту
        # переменную ответ(список json)

        items = json.loads(data)
        item = items[0]  # предполагаю, что в списке json
        # будет только один словарь и обращаюсь
        # к первому элементу(к словарю) спика

        if item['order_status'] == "approved":  # проверяю, если статус платежа успешен,
            # то делаю нужные мне действия с пользователем
            print("Делаем")


@login_required(login_url='accounts/login/')
def black(request):
    # Configuration.configure('873469', 'test_q_nwW-qQ3EihdW3M4NtbXgO4z9yGjMHVilhXbxfdXyY')
    global event
    Configuration.configure_auth_token('AAEAAAAAQX38FQAAAX7SgOI0RoZAUo1DJS2O8uTn6WdJRlfLNWjUfi1R_XwIrSZIpjXYnGfqk9kfZ9PzUPfCyz3O')
    Configuration.configure_user_agent(framework=Version('Django', '3.1.7'))

    whUrl = 'https://test-my-site-id.herokuapp.com/'
    needWebhookList = [
        WebhookNotificationEventType.PAYMENT_SUCCEEDED,
        WebhookNotificationEventType.PAYMENT_CANCELED
    ]

    whList = Webhook.list()

    for event in needWebhookList:
        hookIsSet = False
        for wh in whList.items:
            if wh.event != event:
                continue
            if wh.url != whUrl:
                Webhook.remove(wh.id)
            else:
                hookIsSet = True

        if not hookIsSet:
            Webhook.add({"event": event, "url": whUrl})

    var_dump.var_dump(Webhook.list())
    print(vars(Webhook.list()))

    idempotence_key = str(uuid.uuid4())

    # payment_id = '298c8e3b-000f-5000-9000-1f612ba540bc'
    # payment_one = Payment.find_one(payment_id)

    payment = Payment.create({
        "amount": {
            "value": "2.00",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://127.0.0.1:8000/"
        },

        "id": idempotence_key,
        "capture": True,
        # "response_type": "code",
        # "client_id": "3mo1gntboh51tguf0pphlabe6rfuhh2j",

        "description": "Заказ №72"
    }, )
    print(idempotence_key)
    # print(vars(payment_one))
    confirmation_url = payment.confirmation.confirmation_url

    if request.user.is_authenticated:  # dict_payment['_PaymentResponse__status'] == 'succeeded'
        value, created = Choose.objects.get_or_create(voter=request.user)

        if request.method == 'POST':
            select_action = request.POST['choose']

            if select_action == 'black':
                value.count_black += 1
                value.save()
            return redirect("home")

        if value.count_white > 0 or value.count_black > 0 or value.count_purple > 0:
            return render(request, '403/black.html')

    else:
        return render(request, 'registration/black.html')

    return render(request, 'registration/black_pay.html', {"url": confirmation_url})
def black_results(request):
    # получаем всех голосовавших за черный цвет (1 или более раз)
    black_voters = Choose.objects.filter(count_black__gte=1)

    sum_black = Choose.objects.aggregate(Sum('count_black'))
    sum_white = Choose.objects.aggregate(Sum('count_white'))
    sum_purple = Choose.objects.aggregate(Sum('count_purple'))

    sum_black_result = sum_black['count_black__sum']

    all = sum_black['count_black__sum'] + sum_white['count_white__sum'] + sum_purple['count_purple__sum']
    percent_black = int(sum_black['count_black__sum'] * 100 / all)

    # передаем в шаблон
    paginator = Paginator(black_voters, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'results/black_results.html', {'voters': page_obj, 'page_obj': page_obj, "sum_black_result": sum_black_result, "percent_black": percent_black})


@login_required(login_url='accounts/login/')
def white(request):
    Configuration.configure('873469', 'test_q_nwW-qQ3EihdW3M4NtbXgO4z9yGjMHVilhXbxfdXyY')
    Configuration.configure_user_agent(framework=Version('Django', '3.1.7'))

    idempotence_key = str(uuid.uuid4())

    payment_id = '29886c50-000f-5000-8000-113bdfdebe75'
    payment_one = Payment.find_one(payment_id)

    dict_payment = {'_PaymentResponse__id': '29886c50-000f-5000-8000-113bdfdebe75',
                    '_PaymentResponse__status': 'succeeded'}

    payment = Payment.create({
        "amount": {
            "value": "2.00",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://test-my-site-id.herokuapp.com/"
        },

        "capture": True,

        "description": "Заказ №72"
    }, idempotence_key)

    confirmation_url = payment.confirmation.confirmation_url

    if dict_payment['_PaymentResponse__status'] == 'succeeded':
        value, created = Choose.objects.get_or_create(voter=request.user)

        if request.method == 'POST':
            select_action = request.POST['choose']

            if select_action == 'white':
                value.count_white += 1
                value.save()

            return redirect("home")

        if value.count_white > 0 or value.count_black > 0 or value.count_purple > 0:
            return render(request, '403/white.html')

    else:
        return render(request, 'registration/white_pay.html')

    return render(request, 'registration/white.html', {"url": confirmation_url})


def white_results(request):
    # получаем всех голосовавших за черный цвет (1 или более раз)
    white_voters = Choose.objects.filter(count_white__gte=1)

    sum_black = Choose.objects.aggregate(Sum('count_black'))
    sum_white = Choose.objects.aggregate(Sum('count_white'))
    sum_purple = Choose.objects.aggregate(Sum('count_purple'))

    sum_white_result = sum_white['count_white__sum']

    all = sum_black['count_black__sum'] + sum_white['count_white__sum'] + sum_purple['count_purple__sum']
    percent_white = int(sum_white['count_white__sum'] * 100 / all)

    # передаем в шаблон
    paginator = Paginator(white_voters, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'results/white_results.html', {'voters': page_obj, 'page_obj': page_obj, "sum_white_result": sum_white_result, "percent_white": percent_white})


@login_required(login_url='accounts/login/')
def purple(request):
    Configuration.configure('873469', 'test_q_nwW-qQ3EihdW3M4NtbXgO4z9yGjMHVilhXbxfdXyY')
    Configuration.configure_user_agent(framework=Version('Django', '3.1.7'))

    idempotence_key = str(uuid.uuid4())

    payment_id = '29886c50-000f-5000-8000-113bdfdebe75'
    payment_one = Payment.find_one(payment_id)

    dict_payment = vars(payment_one)

    payment = Payment.create({
        "amount": {
            "value": "2.00",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://test-my-site-id.herokuapp.com/"
        },

        "capture": True,

        "description": "Заказ №72"
    }, idempotence_key)

    confirmation_url = payment.confirmation.confirmation_url

    if dict_payment['_PaymentResponse__status'] == 'succeeded':
        value, created = Choose.objects.get_or_create(voter=request.user)

        if request.method == 'POST':
            select_action = request.POST['choose']

            if select_action == 'purple':
                value.count_purple += 1
                value.save()

            return redirect("home")

        if value.count_white > 0 or value.count_black > 0 or value.count_purple > 0:
            return render(request, '403/purple.html')

    else:
        return render(request, 'registration/purple_pay.html')
    return render(request, 'registration/purple.html', {"url": confirmation_url})

def purple_results(request):
    purple_voters = Choose.objects.filter(count_purple__gte=1)

    sum_black = Choose.objects.aggregate(Sum('count_black'))
    sum_white = Choose.objects.aggregate(Sum('count_white'))
    sum_purple = Choose.objects.aggregate(Sum('count_purple'))

    sum_purple_result = sum_purple['count_purple__sum']

    all = sum_black['count_black__sum'] + sum_white['count_white__sum'] + sum_purple['count_purple__sum']
    percent_purple = int(sum_purple['count_purple__sum'] * 100 / all)

    paginator = Paginator(purple_voters, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'results/purple_results.html', {'voters': page_obj, 'page_obj': page_obj, "sum_purple_result": sum_purple_result, "percent_purple": percent_purple})


class Profile(TemplateView):
    template_name = 'registration/profile.html'

    def get(self, request, username):
        # получаем пользователя по username если он существует
        user = get_object_or_404(User, username=username)
        # передаем его в шаблон как profile
        choose = Choose.objects.filter(voter=user).first()
        return render(request, self.template_name, {"profile": user, 'choose': choose})


class Comment2(TemplateView):
    template_name = "registration/comments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = Comment.objects.get(pk=1)
        somebody, created = Choose.objects.get_or_create(voter=self.request.user)
        context['comment'] = comment
        context['somebody'] = somebody

        return context



