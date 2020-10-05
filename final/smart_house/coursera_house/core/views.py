from django.urls import reverse_lazy
from django.views.generic import FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from marshmallow import Schema, fields
from marshmallow.validate import Range
from marshmallow import ValidationError


from .models import Setting
from .form import ControllerForm
from .tasks import smart_home_manager


class MyBoolean(fields.Boolean):
    truthy = fields.Boolean.truthy.union({"on"})
    falsy = fields.Boolean.falsy.union({"off"})


class ControllerViewSchema(Schema):
    bedroom_target_temperature = fields.Int(validate=Range(16, 50), default=21)
    hot_water_target_temperature = fields.Int(validate=Range(24, 90), default=80)
    bedroom_light = MyBoolean()
    bathroom_light = MyBoolean()


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        try:
            context['data'] = settings.TEMPLATE_DATA['controllers']
            # print(context['data'])
        except ValueError:
            print('Decoding JSON has failed')
        return context

    def get_initial(self):

        params = {
            'bedroom_target_temperature': 21,
            'hot_water_target_temperature': 80,
            'bedroom_light': False,
            'bathroom_light': False
        }
        if Setting.objects.get(controller_name='bedroom_target_temperature'):
            params['bedroom_target_temperature'] = Setting.objects.get(
                controller_name='bedroom_target_temperature').value
        if Setting.objects.get(controller_name='hot_water_target_temperature'):
            params['hot_water_target_temperature'] = Setting.objects.get(
                controller_name='hot_water_target_temperature').value
        smart_home_manager()
        return params

    def form_valid(self, form):
        try:
            schema = ControllerViewSchema(strict=True)
            data = schema.load(self.request.POST)
            bedroom_target_temperature = data.data['bedroom_target_temperature']
            hot_water_target_temperature = data.data['hot_water_target_temperature']
            bedroom_light = False
            bathroom_light = False
            if "bedroom_light" in data.data:
                bedroom_light = data.data["bedroom_light"]

            if "bathroom_light" in data.data:
                bathroom_light = data.data["bathroom_light"]

            if Setting.objects.get(controller_name='bedroom_target_temperature'):
                bedroom_target_temperature_model = Setting.objects.get(controller_name='bedroom_target_temperature')
                bedroom_target_temperature_model.value = bedroom_target_temperature
                bedroom_target_temperature_model.save()
            else:
                bedroom_target_temperature_model = Setting(
                    controller_name='bedroom_target_temperature',
                    label='bedroom_target_temperature',
                    value=bedroom_target_temperature
                )
                bedroom_target_temperature_model.save()

            if Setting.objects.get(controller_name='hot_water_target_temperature'):
                hot_water_target_temperature_model = Setting.objects.get(controller_name='hot_water_target_temperature')
                hot_water_target_temperature_model.value = hot_water_target_temperature
                hot_water_target_temperature_model.save()
            else:
                hot_water_target_temperature_model = Setting(
                    controller_name='hot_water_target_temperature',
                    label='hot_water_target_temperature',
                    value=hot_water_target_temperature
                )
                hot_water_target_temperature_model.save()

        except ValidationError as exc:
            return HttpResponseRedirect('/')
        except ValueError:
            print('Decoding JSON has failed')

        return super(ControllerView, self).form_valid(form)

