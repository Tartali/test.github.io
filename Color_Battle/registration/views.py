import uuid
import json

import var_dump as var_dump
from yookassa import Payment
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory

from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.http import HttpResponseForbidden, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import Choose, Comment


from yookassa import Configuration, Payment
from yookassa.domain.common.user_agent import Version


def home(request):
        value = Choose.objects.all()
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
        }

        return render(request, 'registration/home.html', context)


def callback_payment(request):
    if request.method == 'POST':
        data = request.POST # передаем в эту
        # переменную ответ(список json)

        items = json.loads(data)
        item = items[0] # предполагаю, что в списке json
        # будет только один словарь и обращаюсь
        # к первому элементу(к словарю) спика

        if item['order_status'] == "approved": # проверяю, если статус платежа успешен,
            # то делаю нужные мне действия с пользователем
            print("Делаем")


@login_required(login_url='accounts/login/')
def black(request):
    Configuration.configure('873469', 'test_q_nwW-qQ3EihdW3M4NtbXgO4z9yGjMHVilhXbxfdXyY')
    Configuration.configure_user_agent(framework=Version('Django', '3.1.7'))

    idempotence_key = str(uuid.uuid4())

    # payment_id = '29886c50-000f-5000-8000-113bdfdebe75'
    # payment_one = Payment.find_one(payment_id)
    #
    # dict_payment = vars(payment_one)

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

    event_json = json.loads(request.body)
    try:
        # Создание объекта класса уведомлений в зависимости от события
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика
            # ...
            # if dict_payment['_PaymentResponse__status'] == 'succeeded':
            value, created = Choose.objects.get_or_create(voter=request.user)

            if request.method == 'POST':
                select_action = request.POST['choose']

                if select_action == 'black':
                    value.count_black += 1
                    value.save()
                return redirect("home")

            if value.count_white > 0 or value.count_black > 0 or value.count_purple > 0:
                return render(request, '403/black.html')

            return render(request, 'registration/black.html', {"url": confirmation_url})
        elif notification_object.event == WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
            some_data = {
                'refundId': response_object.id,
                'refundStatus': response_object.status,
                'paymentId': response_object.payment_id,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.DEAL_CLOSED:
            some_data = {
                'dealId': response_object.id,
                'dealStatus': response_object.status,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.PAYOUT_SUCCEEDED:
            some_data = {
                'payoutId': response_object.id,
                'payoutStatus': response_object.status,
                'dealId': response_object.deal.id,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.PAYOUT_CANCELED:
            some_data = {
                'payoutId': response_object.id,
                'payoutStatus': response_object.status,
                'dealId': response_object.deal.id,
            }
            # Специфичная логика
            # ...
        else:
            # Обработка ошибок
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

        # Специфичная логика
        # ...
        Configuration.configure('XXXXXX', 'test_XXXXXXXX')
        # Получим актуальную информацию о платеже
        payment_info = Payment.find_one(some_data['paymentId'])
        if payment_info:
            payment_status = payment_info.status
            # Специфичная логика
            # ...
        else:
            # Обработка ошибок
            return HttpResponse(status=400)  # Сообщаем кассе об ошибке

    except Exception:
        # Обработка ошибок
        return HttpResponse(status=400)  # Сообщаем кассе об ошибке

    return HttpResponse(status=200)  # Сообщаем кассе, что все хорошо

    # # if dict_payment['_PaymentResponse__status'] == 'succeeded':
    #     value, created = Choose.objects.get_or_create(voter=request.user)
    #
    #     if request.method == 'POST':
    #         select_action = request.POST['choose']
    #
    #         if select_action == 'black':
    #             value.count_black += 1
    #             value.save()
    #         return redirect("home")
    #
    #     if value.count_white > 0 or value.count_black > 0 or value.count_purple > 0:
    #         return render(request, '403/black.html')
    #
    # else:
    #     return render(request, 'registration/black_pay.html')
    #
    # return render(request, 'registration/black.html', {"url": confirmation_url})


def black_results(request):
    # получаем всех голосовавших за черный цвет (1 или более раз)
    black_voters = Choose.objects.filter(count_black__gte=1)
    # передаем в шаблон
    return render(request, 'results/black_results.html',)


@login_required(login_url='accounts/login/')
def white(request):
    Configuration.configure('873469', 'test_q_nwW-qQ3EihdW3M4NtbXgO4z9yGjMHVilhXbxfdXyY')
    Configuration.configure_user_agent(framework=Version('Django', '3.1.7'))

    idempotence_key = str(uuid.uuid4())

    payment_id = '29886c50-000f-5000-8000-113bdfdebe75'
    payment_one = Payment.find_one(payment_id)

    dict_payment = {'_PaymentResponse__id': '29886c50-000f-5000-8000-113bdfdebe75', '_PaymentResponse__status': 'succeeded'}

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
    # передаем в шаблон
    return render(request, 'results/white_results.html', {'voters': white_voters})


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
        context = super(Comment2, self).get_context_data(**kwargs)
        comment = Comment.objects.get(pk=1)
        context['comment'] = comment
        return context