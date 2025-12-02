from rest_framework import status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema, inline_serializer
from drf_spectacular.types import OpenApiTypes
from django.conf import settings

from . import utils


# -------------------- SYSTEM -------------------- #
class CheckApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Проверка доступности API",
        description="Простая проверка, что сервис жив.",
        responses={
            200: inline_serializer(
                name="CheckResponse",
                fields={"status": serializers.CharField()}
            )
        },
    )
    def get(self, request: Request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


# -------------------- TEAM -------------------- #
class TeamInfoApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Информация о команде",
        description="Возвращает основную информацию о текущей команде (Virtus.pro и т.п.).",
        request=None,
        responses={
            200: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request: Request):
        try:
            team_info = utils.get_team_info()
            return Response(
                data={"status": "ok", "team_info": team_info},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TeamMatchesApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Матчи команды",
        description="Возвращает список матчей команды за период/по умолчанию (реализация в utils.get_team_matches).",
        request=None,
        responses={
            200: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request: Request):
        try:
            team_matches = utils.get_team_matches()
            return Response(
                data={"status": "ok", "team_matches": team_matches},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# -------------------- PLAYER -------------------- #
class SearchPlayerApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Поиск игрока",
        description="Поиск игрока по имени через HLTV.",
        request=inline_serializer(
            name="SearchPlayerRequest",
            fields={
                "name": serializers.CharField(help_text="Ник/имя игрока, например 'FL1T'"),
            }
        ),
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request):
        try:
            name = request.data.get("name")
            if not name:
                return Response(
                    data={"error": "name is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            player = utils.search_player(name=name)
            return Response(
                data={"status": "ok", "player": player},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PlayerProfileApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Профиль игрока",
        description="Возвращает профиль игрока по его HLTV id и имени.",
        request=inline_serializer(
            name="PlayerProfileRequest",
            fields={
                "id": serializers.CharField(help_text="HLTV ID игрока, например '12732'"),
                "name": serializers.CharField(help_text="Имя/ник игрока, например 'FL1T'"),
            }
        ),
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request):
        try:
            id = request.data.get("id")
            name = request.data.get("name")
            if not id or not name:
                return Response(
                    data={"error": "name and id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            player_profile = utils.get_player_profile(id=id, player_name=name)
            return Response(
                data={"status": "ok", "player_profile": player_profile},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PlayerStatApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Статистика игрока",
        description="Возвращает overview-статистику игрока по HLTV id и имени.",
        request=inline_serializer(
            name="PlayerStatsRequest",
            fields={
                "id": serializers.CharField(help_text="HLTV ID игрока"),
                "name": serializers.CharField(help_text="Имя/ник игрока"),
            }
        ),
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request):
        try:
            id = request.data.get("id")
            name = request.data.get("name")
            if not id or not name:
                return Response(
                    data={"error": "name and id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            player_stat = utils.get_player_stats_overview(id=id, player_name=name)
            return Response(
                data={"status": "ok", "player_stat": player_stat},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# -------------------- MATCHES -------------------- #
class GetUpcomingMatchesApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Ближайшие матчи",
        description="Возвращает список ближайших матчей (реализация в utils.get_upcoming_matches).",
        request=None,
        responses={
            200: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request: Request):
        try:
            upcoming_matches = utils.get_upcoming_matches()
            return Response(
                data={"status": "ok", "upcoming_matches": upcoming_matches},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetMatchDetailsApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Детали матча",
        description="Возвращает полные детали матча по HLTV id и slug'у матча.",
        request=inline_serializer(
            name="MatchDetailsRequest",
            fields={
                "id": serializers.CharField(help_text="HLTV ID матча, например '2372341'"),
                "match_name": serializers.CharField(help_text="Slug матча, например 'virtuspro-vs-big-iem-dallas-2024'"),
            }
        ),
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request):
        try:
            id = request.data.get("id")
            match_name = request.data.get("match_name")
            if not id or not match_name:
                return Response(
                    data={"error": "match_name and id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            match_details = utils.get_match_details(id=id, match_name=match_name)
            return Response(
                data={"status": "ok", "match_details": match_details},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# -------------------- TABLEAU -------------------- #
class GetTableauCTSideApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="CT-side Tableau данные",
        description="Читает файл ct_side.csv из локальной FS и возвращает его как список dict'ов.",
        request=None,
        responses={
            200: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request: Request):
        try:
            t_side = utils.csv_to_dict_from_path(settings.BASE_DIR / 'api/tableau/ct_side.csv')
            return Response(
                data={"status": "ok", "t_side": t_side},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetTableauTSideApiAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="T-side Tableau данные",
        description="Читает файл t_side.csv из локальной FS и возвращает его как список dict'ов.",
        request=None,
        responses={
            200: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request: Request):
        try:
            t_side = utils.csv_to_dict_from_path(settings.BASE_DIR / 'api/tableau/t_side.csv')
            return Response(
                data={"status": "ok", "t_side": t_side},
                status=status.HTTP_200_OK
            )

        except Exception as ex:
            return Response(
                data={"status": "error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
