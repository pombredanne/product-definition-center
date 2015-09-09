#
# Copyright (c) 2015 Red Hat
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#
from pdc.apps.common import viewsets
from .models import Person, Maillist, ContactRole
from .serializers import (PersonSerializer, MaillistSerializer,
                          ContactRoleSerializer)
from .filters import PersonFilterSet, MaillistFilterSet, ContactRoleFilterSet


# Create your views here.
class PersonViewSet(viewsets.PDCModelViewSet):
    """
    ##Overview##

    This page shows the usage of the **Person API**, please see the
    following for more details.

    ##Test tools##

    You can use ``curl`` in terminal, with -X _method_ (GET|POST|PUT|PATCH|DELETE),
    -d _data_ (a json string). or GUI plugins for
    browsers, such as ``RESTClient``, ``RESTConsole``.
    """

    def create(self, request, *args, **kwargs):
        """
        ### CREATE

        __Method__:
        POST

        __URL__: $LINK:person-list$

        __Data__:

        %(WRITABLE_SERIALIZER)s

        __Response__:

        %(SERIALIZER)s

        __Example__:

            curl -H "Content-Type: application/json"  -X POST -d '{"username": "test", "email": "test@example.com"}' $URL:person-list$
            # output
            {"id": 1, "username": "test", "email": "test@example.com"}
        """
        return super(PersonViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        ### LIST

        __Method__:
        GET

        __URL__: $LINK:person-list$

        __Query Params__:

        %(FILTERS)s

        __Response__: a paged list of following objects

        %(SERIALIZER)s
        """
        return super(PersonViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        ### RETRIEVE

        __Method__:
        GET

        __URL__: $LINK:person-detail:instance_pk$

        __Response__:

        %(SERIALIZER)s

        __Example__:

            curl -H "Content-Type: application/json" $URL:person-detail:1$
            # output
            {"id": 1, "username": "test", "email": "test@example.com"}
        """
        return super(PersonViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        ### UPDATE

        __Method__: `PUT`, `PATCH`

        __URL__: $LINK:person-detail:instance_pk$

        __Data__:

        %(WRITABLE_SERIALIZER)s

        __Response__:

        %(SERIALIZER)s

        __Example__:

        PUT:

            curl -X PUT -d '{"username": "new_name", "email": "new_email"}' -H "Content-Type: application/json" $URL:person-detail:1$
            # output
            {"id": 1, "username": "new_name", "email": "new_email"}

        PATCH:

            curl -X PATCH -d '{"email": "new_email"}' -H "Content-Type: application/json" $URL:person-detail:1$
            # output
            {"id": 1, "username": "name", "email": "new_email"}
        """
        return super(PersonViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        ### DELETE

        __Method__:
        DELETE

        __URL__: $LINK:person-detail:instance_pk$

        __Response__:

            STATUS: 204 NO CONTENT

        __Example__:

            curl -X DELETE -H "Content-Type: application/json" $URL:person-detail:1$
        """
        return super(PersonViewSet, self).destroy(request, *args, **kwargs)

    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    filter_class = PersonFilterSet


class MaillistViewSet(viewsets.PDCModelViewSet):
    """
    ##Overview##

    This page shows the usage of the **Maillist API**, please see the
    following for more details.

    ##Test tools##

    You can use ``curl`` in terminal, with -X _method_ (GET|POST|PUT|PATCH|DELETE),
    -d _data_ (a json string). or GUI plugins for
    browsers, such as ``RESTClient``, ``RESTConsole``.
    """

    def create(self, request, *args, **kwargs):
        """
        ### CREATE

        __Method__:
        POST

        __URL__: $LINK:maillist-list$

        __Data__:

        %(WRITABLE_SERIALIZER)s

        __Response__:

        %(SERIALIZER)s

        __Example__:

            curl -H "Content-Type: application/json"  -X POST -d '{"mail_name": "test", "email": "test@example.com"}' $URL:maillist-list$
            # output
            {"id": 1, "mail_name": "test", "email": "test@example.com"}
        """
        return super(MaillistViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        ### LIST

        __Method__:
        GET

        __URL__: $LINK:maillist-list$

        __Query Params__:

        %(FILTERS)s

        __Response__: a paged list of following objects

        %(SERIALIZER)s

        __Example__:

        With query params:

            curl -H "Content-Type: application/json"  -G $URL:maillist-list$ --data-urlencode "mail_name=test"
            # output
            {
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "id": int,
                        "mail_name": "test",
                        "email": "test@example.com"
                    }
                ]
            }
        """
        return super(MaillistViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        ### RETRIEVE

        __Method__:
        GET

        __URL__: $LINK:maillist-detail:instance_pk$

        __Response__:

        %(SERIALIZER)s

        __Example__:

            curl -H "Content-Type: application/json" $URL:maillist-detail:1$
            # output
            {"id": 1, "mail_name": "test", "email": "test@example.com"}
        """
        return super(MaillistViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        ### UPDATE

        __Method__: `PUT`, `PATCH`
        PUT: for full fields update
            {'mail_name': 'new_name', 'email': 'new_email'}

        PATCH: for partial update
            {'mail_name': 'new_name'}
            or
            {'email': 'new_email'}
            or
            {'mail_name': 'new_name', 'email': 'new_email'}

        __URL__: $LINK:maillist-detail:instance_pk$

        __Data__:

        %(WRITABLE_SERIALIZER)s

        __Response__:

        %(SERIALIZER)s

        __Example__:

        PUT:

            curl -X PUT -d '{"mail_name": "new_name", "email": "new_email"}' -H "Content-Type: application/json" $URL:maillist-detail:1$
            # output
            {"id": 1, "mail_name": "new_name", "email": "new_email"}

        PATCH:

            curl -X PATCH -d '{"email": "new_email"}' -H "Content-Type: application/json" $URL:maillist-detail:1$
            # output
            {"id": 1, "mail_name": "name", "email": "new_email"}
        """
        return super(MaillistViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        ### DELETE

        __Method__:
        DELETE

        __URL__: $LINK:maillist-detail:instance_pk$

        __Response__:

            STATUS: 204 NO CONTENT

        __Example__:

            curl -X DELETE -H "Content-Type: application/json" $URL:maillist-detail:1$
        """
        return super(MaillistViewSet, self).destroy(request, *args, **kwargs)

    serializer_class = MaillistSerializer
    queryset = Maillist.objects.all()
    filter_class = MaillistFilterSet


class ContactRoleViewSet(viewsets.PDCModelViewSet):
    """
    ##Overview##

    This page shows the usage of the **Contact Role API**, please see the
    following for more details.

    ##Test tools##

    You can use ``curl`` in terminal, with -X _method_ (GET|POST|PUT|PATCH|DELETE),
    -d _data_ (a json string). or GUI plugins for
    browsers, such as ``RESTClient``, ``RESTConsole``.
    """

    def create(self, request, *args, **kwargs):
        """
        ### CREATE

        __Method__:
        POST

        __URL__: $LINK:contactrole-list$

        __Data__:

        %(WRITABLE_SERIALIZER)s

        __Response__:

        %(SERIALIZER)s

        __Example__:

            curl -H "Content-Type: application/json"  -X POST -d '{"name": "test"}' $URL:contactrole-list$
            # output
            {"name": "test"}
        """
        return super(ContactRoleViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        ### LIST

        __Method__:
        GET

        __URL__: $LINK:contactrole-list$

        __Query Params__:

        %(FILTERS)s

        __Response__: a paged list of following objects

        %(SERIALIZER)s

        __Example__:

            curl -H "Content-Type: application/json"  -X GET $URL:contactrole-list$
            # output
            {
                "count": 4,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "name": "qe_leader",
                    },
                    {
                        "name": "qe_group",
                    },
                    ...
                ]
            }

        With query params:

            curl -H "Content-Type: application/json"  -G $URL:contactrole-list$ --data-urlencode "name=test"
            # output
            {
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "name": "test",
                    }
                ]
            }
        """
        return super(ContactRoleViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        ### RETRIEVE

        __Method__:
        GET

        __URL__: $LINK:contactrole-detail:role_name$

        __Response__:

        %(SERIALIZER)s

        __Example__:

            curl -H "Content-Type: application/json" $URL:contactrole-detail:QE_Leader$
            # output
            {"name": "QE_Leader"}
        """
        return super(ContactRoleViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        ### UPDATE

        __Method__: `PUT`, `PATCH`

        __URL__: $LINK:contactrole-detail:role_name$

        __Data__:

        %(WRITABLE_SERIALIZER)s

        __Response__:

        %(SERIALIZER)s

        __Example__:

        PUT:

            curl -X PUT -d '{"name": "new_name"}' -H "Content-Type: application/json" $URL:contactrole-detail:QE_Ack$
            # output
            {"name": "new_name"}

        PATCH:

            curl -X PATCH -d '{"name": "new_name"}' -H "Content-Type: application/json" $URL:contactrole-detail:QE_Ack$
            # output
            {"name": "new_name"}
        """
        return super(ContactRoleViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        ### DELETE

        __Method__:
        DELETE

        __URL__: $LINK:contactrole-detail:role_name$

        __Response__:

            STATUS: 204 NO CONTENT

        __Example__:

            curl -X DELETE -H "Content-Type: application/json" $URL:contactrole-detail:QE_Group$
        """
        return super(ContactRoleViewSet, self).destroy(request, *args, **kwargs)

    serializer_class = ContactRoleSerializer
    queryset = ContactRole.objects.all()
    filter_class = ContactRoleFilterSet
    lookup_field = 'name'
    overwrite_lookup_field = False
