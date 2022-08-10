from rest_framework import mixins, viewsets


class CreateDeleteListViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    pass
