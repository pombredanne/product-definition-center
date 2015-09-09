#
# Copyright (c) 2015 Red Hat
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#
import json

from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from pdc.apps.common.serializers import DynamicFieldsSerializerMixin, StrictSerializerMixin
from .models import ContactRole, Person, Maillist


class ContactRoleSerializer(StrictSerializerMixin,
                            serializers.HyperlinkedModelSerializer):
    name = serializers.SlugField()

    class Meta:
        model = ContactRole
        fields = ('name', )


class PersonSerializer(DynamicFieldsSerializerMixin,
                       StrictSerializerMixin,
                       serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Person
        fields = ('id', 'username', 'email')


class MaillistSerializer(DynamicFieldsSerializerMixin,
                         StrictSerializerMixin,
                         serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Maillist
        fields = ('id', 'mail_name', 'email')


class ContactField(serializers.DictField):
    child = serializers.CharField()
    field_to_class = {
        "username": Person,
        "mail_name": Maillist,
    }
    class_to_serializer = {
        "Person": PersonSerializer,
        "Maillist": MaillistSerializer,
    }

    def to_representation(self, value):
        leaf_value = value.as_leaf_class()
        serializer_cls = self.class_to_serializer.get(
            type(leaf_value).__name__, None)
        if serializer_cls:
            leaf_serializer = serializer_cls(exclude_fields=['url'],
                                             context=self.context)
            return leaf_serializer.to_representation(leaf_value)
        else:
            raise serializers.ValidationError("Unsupported Contact: %s" % value)

    def to_internal_value(self, data):
        v_data = super(ContactField, self).to_internal_value(data)
        for key, clazz in self.field_to_class.items():
            if key in v_data:
                contact, created = clazz.objects.get_or_create(**v_data)
                if created:
                    request = self.context.get('request', None)
                    model_name = ContentType.objects.get_for_model(contact).model
                    if request:
                        request.changeset.add(model_name,
                                              contact.id,
                                              'null',
                                              json.dumps(contact.export()))
                return contact
        raise serializers.ValidationError('Could not determine type of contact.')
