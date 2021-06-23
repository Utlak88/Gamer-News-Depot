import json
import random
import re
from datetime import datetime
from itertools import zip_longest
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.shortcuts import render
from django_celery_results.models import TaskResult
from homepage.models import Dev
from users.forms import FavoriteGamesUpdateForm
from users.models import Profile, FavoriteGames


def dev_view(request, slug=""):
    """View for homepage or individual developer."""
    if slug == "":

        dev_name = list(Dev.objects.all().values_list('dev_name', flat=True))
        dev_img_address = list(Dev.objects.values_list('dev_image_address', flat=True))
        dev_slug = list(Dev.objects.values_list('dev_slug', flat=True))
        dev_order = list(Dev.objects.values_list('dev_order_pop', flat=True))

        if len(list(TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_query').values())) == 1:
            g_query_datetime_init = list(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_query'
            ).values_list()[0])
        else:
            task_id_query = list(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_query'
            ).values())[1]['task_id']

            g_query_datetime_init = list(TaskResult.objects.filter(
                task_id=task_id_query
            ).values_list()[0])

        g_query_datetime = g_query_datetime_init[11]

        if len(list(TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_dev').values())) == 1:
            g_dev_datetime_init = list(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_dev'
            ).values_list()[0])
        else:
            task_id_dev = list(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_dev'
            ).values())[1]['task_id']

            g_dev_datetime_init = list(TaskResult.objects.filter(
                task_id=task_id_dev
            ).values_list()[0])

        g_dev_datetime = g_dev_datetime_init[11]

        if g_dev_datetime > g_query_datetime:
            g_datetime = g_dev_datetime
        elif g_dev_datetime < g_query_datetime:
            g_datetime = g_query_datetime

        if len(list(TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_query').values())) == 1:
            g_query = json.loads(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_query'
            ).values()[0]['result'])
        else:
            task_id_query = list(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_query'
            ).values())[1]['task_id']

            g_query = json.loads(TaskResult.objects.filter(
                task_id=task_id_query
            ).values()[0]['result'])

        if len(list(TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_dev').values())) == 1:
            g_dev = json.loads(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_dev'
            ).values()[0]['result'])
        else:
            task_id_dev = list(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_dev'
            ).values())[1]['task_id']

            g_dev = json.loads(TaskResult.objects.filter(
                task_id=task_id_dev
            ).values()[0]['result'])

        # 2-day date filter for homepage 'Latest News'
        def date_criteria(g_inp):
            dates = [re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', g_inp[i][8]).group(0) for i in range(len(g_inp))]
            dates_datetime = [datetime.strptime(i, '%Y-%m-%d') for i in dates]

            today = datetime.today()
            time_criteria = datetime(year=today.year, month=today.month, day=today.day - 2)

            return [g_inp[i] for i in range(len(g_inp)) if dates_datetime[i] >= time_criteria]

        entries_for_carousel_init = [date_criteria(g_dev) + date_criteria(g_query)][0]
        entries_for_carousel = [i for i in entries_for_carousel_init if i[9] != 'none']
        entries_for_latest_news_init = entries_for_carousel
        entries_for_latest_news_init = sorted(entries_for_latest_news_init, key=lambda sort: sort[8], reverse=True)
        link_latest_news = [i[1] for i in entries_for_latest_news_init]
        link_count = [link_latest_news.count(link_latest_news[i]) for i in
                      range(len(link_latest_news))]
        link_zip = list(zip(link_latest_news, link_count))
        link_unique = [link_zip[i][0] if link_zip[i][1] == 1 else 'none' for i in
                       range(len(link_zip))]
        nonunique_indices_link = [i for i, x in enumerate(link_unique) if x == "none"]
        nonunique_check_link = []
        nonunique_entries_nonrepeat_link = []

        for i in nonunique_indices_link:
            nonunique_check_link.append(link_latest_news[i])
            count_inst = nonunique_check_link.count(link_latest_news[i])
            if count_inst == 1:
                nonunique_entries_nonrepeat_link.append(entries_for_latest_news_init[i])

        google_search_results_unique = []

        for i in range(len(link_unique)):
            try:
                if link_unique[i] != 'none':
                    google_search_results_unique.append(entries_for_latest_news_init[i])
            except IndexError:
                pass

        google_search_results_combined = google_search_results_unique + nonunique_entries_nonrepeat_link
        page = request.GET.get('page', 1)
        paginator2 = Paginator(google_search_results_combined, 2000)

        try:
            entries_for_latest_news = paginator2.page(page)
        except PageNotAnInteger:
            entries_for_latest_news = paginator2.page(1)
        except EmptyPage:
            entries_for_latest_news = paginator2.page(paginator2.num_pages)

        random.shuffle(entries_for_carousel)

        if request.user.is_authenticated:
            if request.method == "POST":
                p_form = FavoriteGamesUpdateForm(data=request.POST)
                user_fav = list(FavoriteGames.objects.all().values_list())
                user_slug_list = [user_fav[i][2] for i in range(len(user_fav))
                                  if user_fav[i][1] == request.user.profile.id]
                if request.POST["dev_user_str"] not in user_slug_list:
                    if p_form.is_valid():
                        form_instance = p_form.save(commit=False)
                        form_instance.profile = Profile.objects.get(user=request.user)
                        form_instance.dev_user_str = p_form.cleaned_data["dev_user_str"]
                        form_instance.save()
                else:
                    FavoriteGames.objects.filter(
                        profile_id=request.user.profile.id
                    ).filter(
                        dev_user_str=request.POST.get('dev_user_str')
                    ).delete()
            fav_game_check = list(FavoriteGames.objects.filter(profile_id=request.user.profile.id).values())
            devs_in_favs = [fav_game_check[i]['dev_user_str'] for i in range(len(fav_game_check))]
            dev_game_check_list = []
            for j, i in enumerate(dev_slug):
                if i in devs_in_favs:
                    dev_game_check_list.append('yes')
                else:
                    dev_game_check_list.append('no')
        else:
            dev_game_check_list = ""

        dev_list_name = sorted(list(zip_longest(dev_name, dev_img_address, dev_slug, dev_game_check_list, dev_order)),
                               key=lambda lowercase: lowercase[0].lower())
        dev_list_pop = sorted(list(zip_longest(dev_name, dev_img_address, dev_slug, dev_game_check_list, dev_order)),
                              key=lambda dev_order_list: dev_order_list[4])
        cache_key = "test_cache_key"

        if cache.get(cache_key) is not None:
            paginator_for_class_1 = Paginator(cache.get(cache_key), 48)
        else:
            cache.set(
                cache_key,
                dev_list_pop,
                60 * 60 * 4,
            )

        context = {
            'numbers': dev_list_pop,
            'entries': entries_for_carousel,
            'latest_news': entries_for_latest_news,
            'g_query_datetime': g_query_datetime,
            'g_dev_datetime': g_dev_datetime,
            'g_datetime': g_datetime,
        }

        if request.method == "POST":
            return redirect("/")
        else:
            return render(request, "homepage/dev_base.html", context)
    else:
        dev_query_results_init = TaskResult.objects.filter(task_name='homepage.tasks.rawg_fetch_dev')
        dev_query_results = json.loads(dev_query_results_init.values()[0]['result'])

        if len(list(TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_dev').values())) == 1:
            g_dev_datetime_init = list(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_dev'
            ).values_list()[0])
        else:
            task_id_dev = list(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_dev'
            ).values())[1]['task_id']
            g_dev_datetime_init = list(TaskResult.objects.filter(
                task_id=task_id_dev
            ).values_list()[0])

        g_dev_datetime = g_dev_datetime_init[11]
        slug_index1 = [dev_query_results][0][0].index(slug)
        dev_list = [dev_query_results[0][slug_index1]]
        slugs_per_dev_list = dev_query_results[1][slug_index1]
        names_per_dev_list = dev_query_results[2][slug_index1]
        ratings_per_dev_list = dev_query_results[3][slug_index1]
        background_img_per_dev_list = dev_query_results[4][slug_index1]
        released_per_dev_list = dev_query_results[5][slug_index1]
        full_clip_per_dev_list = dev_query_results[6][slug_index1]
        ratings_count_per_dev_list = dev_query_results[7][slug_index1]
        dev_game_data = sorted(list(zip_longest(dev_list, slugs_per_dev_list, names_per_dev_list,
                                                ratings_per_dev_list, background_img_per_dev_list,
                                                released_per_dev_list,
                                                full_clip_per_dev_list, ratings_count_per_dev_list)),
                               key=lambda sort: sort[7], reverse=True)

        dev_game_data2 = []

        for i in range(len(dev_game_data)):
            try:
                if dev_game_data[i][4] is not None:
                    dev_game_data2.append(dev_game_data[i])
            except IndexError:
                pass

        page = request.GET.get('page', 1)
        paginator2 = Paginator(dev_game_data2, 2000)

        try:
            numbers = paginator2.page(page)
        except PageNotAnInteger:
            numbers = paginator2.page(1)
        except EmptyPage:
            numbers = paginator2.page(paginator2.num_pages)

        if len(list(TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_dev').values())) == 1:
            google_query_results = json.loads(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_dev'
            ).values()[0]['result'])
        else:
            task_id_dev = list(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_dev'
            ).values())[1]['task_id']

            google_query_results = json.loads(TaskResult.objects.filter(
                task_id=task_id_dev
            ).values()[0]['result'])

        dev_name_list = list(Dev.objects.all().values_list('dev_name', flat=True))
        dev_slug_list = list(Dev.objects.all().values_list('dev_slug', flat=True))
        dev_img_list = list(Dev.objects.values_list('dev_image_address', flat=True))
        dev_slug_index = dev_slug_list.index(slug)
        dev_name_for_site = dev_name_list[dev_slug_index]
        dev_img_for_site = dev_img_list[dev_slug_index]
        google_search_results = [google_query_results[i] if google_query_results[i][6] == slug else 'none'
                                 for i in range(len(google_query_results))]

        google_search_results2 = []

        for i in range(len(google_search_results)):
            try:
                if google_search_results[i] != 'none':
                    google_search_results2.append(google_search_results[i])
            except IndexError:
                pass

        context = {
            'numbers': numbers,
            'google_search_results': google_search_results2,
            'dev_name_for_site': dev_name_for_site,
            'dev_img_for_site': dev_img_for_site,
            'g_dev_datetime': g_dev_datetime,
        }

        return render(request, "homepage/dev_iter.html", context)


# Example of class-based view to populate all game news (note: this view wasn't used because the task run completion
# time stamp would not auto-update on the production site in a responsive manner (i.e., hours would pass before
# timestamp would update). The function view, by contrast, updates immediately upon a new task running and completing.

# class GameNews(ListView):
#     g_query_datetime_init = list(TaskResult.objects.filter(
#         task_name='homepage.tasks.google_fetch_query'
#     ).values_list()[0])
#     g_query_datetime = g_query_datetime_init[11]
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['g_query_datetime'] = self.g_query_datetime
#         return context
#
#     queryset = json.loads(TaskResult.objects.filter(
#         task_name='homepage.tasks.google_fetch_query'
#     ).values()[0]['result'])
#     paginate_by = 100
#     context_object_name = 'numbers'
#     template_name = 'homepage/popular_news.html'


def gamenews(request):
    """Populate all game news."""

    if len(list(TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_query').values())) == 1:
        g_query_datetime_init = list(TaskResult.objects.filter(
            task_name='homepage.tasks.google_fetch_query'
        ).values_list()[0])
    else:
        task_id_query = list(TaskResult.objects.filter(
            task_name='homepage.tasks.google_fetch_query'
        ).values())[1]['task_id']

        g_query_datetime_init = list(TaskResult.objects.filter(
            task_id=task_id_query
        ).values_list()[0])

    g_query_datetime = g_query_datetime_init[11]

    if len(list(TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_query').values())) == 1:
        queryset = json.loads(TaskResult.objects.filter(
            task_name='homepage.tasks.google_fetch_query'
        ).values()[0]['result'])
    else:
        task_id_query = list(TaskResult.objects.filter(
            task_name='homepage.tasks.google_fetch_query'
        ).values())[1]['task_id']

        queryset = json.loads(TaskResult.objects.filter(
            task_id=task_id_query
        ).values()[0]['result'])

    page = request.GET.get('page', 1)
    paginator2 = Paginator(queryset, 100)

    try:
        numbers = paginator2.page(page)
    except PageNotAnInteger:
        numbers = paginator2.page(1)
    except EmptyPage:
        numbers = paginator2.page(paginator2.num_pages)

    context = {
        'numbers': numbers,
        'g_query_datetime': g_query_datetime,
    }

    return render(request, 'homepage/popular_news.html', context)


# Example of class-based view to populate all developer news (note: this view wasn't used because the task run
# completion time stamp would not auto-update on the production site in a responsive manner (i.e., hours would pass
# before timestamp would update). The function view, by contrast, updates immediately upon a new task running and
# completing.

# class DevGames(ListView):
#     g_dev_datetime_init = list(TaskResult.objects.filter(
#         task_name='homepage.tasks.google_fetch_dev'
#     ).values_list()[0])
#     g_dev_datetime = g_dev_datetime_init[11]
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['g_dev_datetime'] = self.g_dev_datetime
#         return context
#
#     queryset = json.loads(TaskResult.objects.filter(
#         task_name='homepage.tasks.google_fetch_dev'
#     ).values()[0]['result'])
#     paginate_by = 100
#     context_object_name = 'numbers'
#     template_name = 'homepage/dev_all.html'


def devgamesfunct(request):
    if len(list(TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_dev').values())) == 1:
        g_dev_datetime_init = list(TaskResult.objects.filter(
            task_name='homepage.tasks.google_fetch_dev'
        ).values_list()[0])
    else:
        task_id_dev = list(TaskResult.objects.filter(
            task_name='homepage.tasks.google_fetch_dev'
        ).values())[1]['task_id']

        g_dev_datetime_init = list(TaskResult.objects.filter(
            task_id=task_id_dev
        ).values_list()[0])

    g_dev_datetime = g_dev_datetime_init[11]

    if len(list(TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_dev').values())) == 1:
        queryset = json.loads(TaskResult.objects.filter(
            task_name='homepage.tasks.google_fetch_dev'
        ).values()[0]['result'])
    else:
        task_id_dev = list(TaskResult.objects.filter(
            task_name='homepage.tasks.google_fetch_dev'
        ).values())[1]['task_id']

        queryset = json.loads(TaskResult.objects.filter(
            task_id=task_id_dev
        ).values()[0]['result'])

    page = request.GET.get('page', 1)
    paginator2 = Paginator(queryset, 100)

    try:
        numbers = paginator2.page(page)
    except PageNotAnInteger:
        numbers = paginator2.page(1)
    except EmptyPage:
        numbers = paginator2.page(paginator2.num_pages)

    context = {
        'numbers': numbers,
        'g_dev_datetime': g_dev_datetime,
    }

    return render(request, 'homepage/dev_all.html', context)


def dev_list(request):
    """Populate complete list of developers."""

    dev_name = list(Dev.objects.all().values_list('dev_name', flat=True))
    dev_img_address = list(Dev.objects.values_list('dev_image_address', flat=True))
    dev_slug = list(Dev.objects.values_list('dev_slug', flat=True))
    dev_order = list(Dev.objects.values_list('dev_order_pop', flat=True))

    if request.user.is_authenticated:
        if request.method == "POST":
            p_form = FavoriteGamesUpdateForm(data=request.POST)
            user_fav = list(FavoriteGames.objects.all().values_list())
            user_slug_list = [user_fav[i][2] for i in range(len(user_fav))
                              if user_fav[i][1] == request.user.profile.id]

            if request.POST["dev_user_str"] not in user_slug_list:

                if p_form.is_valid():
                    form_instance = p_form.save(commit=False)
                    form_instance.profile = Profile.objects.get(user=request.user)
                    form_instance.dev_user_str = p_form.cleaned_data["dev_user_str"]
                    form_instance.save()
            else:
                FavoriteGames.objects.filter(
                    profile_id=request.user.profile.id
                ).filter(
                    dev_user_str=request.POST.get('dev_user_str')
                ).delete()

        fav_game_check = list(FavoriteGames.objects.filter(profile_id=request.user.profile.id).values())
        devs_in_favs = [fav_game_check[i]['dev_user_str'] for i in range(len(fav_game_check))]

        dev_game_check_list = []

        for j, i in enumerate(dev_slug):
            if i in devs_in_favs:
                dev_game_check_list.append('yes')
            else:
                dev_game_check_list.append('no')

    else:
        dev_game_check_list = ""

    dev_list_name = sorted(list(zip_longest(dev_name, dev_img_address, dev_slug, dev_game_check_list, dev_order)),
                           key=lambda lowercase: lowercase[0].lower())

    dev_list_pop = sorted(list(zip_longest(dev_name, dev_img_address, dev_slug, dev_game_check_list, dev_order)),
                          key=lambda dev_order_list: dev_order_list[4])
    cache_key = "test_cache_key"

    if cache.get(cache_key) is not None:
        paginator_for_class_1 = Paginator(cache.get(cache_key), 48)
    else:
        cache.set(
            cache_key,
            dev_list_pop,
            60 * 60 * 4,
        )

    context = {'numbers': dev_list_pop}

    if request.method == "POST":
        return redirect("/developers")
    else:
        return render(request, "homepage/devs_indiv.html", context)


@login_required
def dev_user(request, slug=""):
    """View that allows user to interact with 'liked' developers."""
    if slug == "":

        user_fav = list(FavoriteGames.objects.all().values_list())
        user_slug_list = [user_fav[i][2] for i in range(len(user_fav)) if user_fav[i][1] == request.user.profile.id]
        dev_name = list(Dev.objects.all().values_list('dev_name', flat=True))
        dev_img_address = list(Dev.objects.values_list('dev_image_address', flat=True))
        dev_slug = list(Dev.objects.values_list('dev_slug', flat=True))
        dev_order = list(Dev.objects.values_list('dev_order_pop', flat=True))
        dev_list_init = [[dev_name[i], dev_img_address[i], dev_slug[i], dev_order[i]] for i in range(len(dev_name))]
        dev_list = [dev_list_init[i] for i in range(len(dev_list_init)) if dev_list_init[i][2] in user_slug_list]
        dev_name = [dev_list[i][0] for i in range(len(dev_list))]
        dev_img_address = [dev_list[i][1] for i in range(len(dev_list))]
        dev_slug = [dev_list[i][2] for i in range(len(dev_list))]
        dev_order = [dev_list[i][3] for i in range(len(dev_list))]

        if request.user.is_authenticated:
            if request.method == "POST":
                p_form = FavoriteGamesUpdateForm(data=request.POST)
                if not (
                        FavoriteGames.objects.filter(
                            dev_user_str=request.POST["dev_user_str"]
                        ).exists()
                ):

                    if p_form.is_valid():
                        form_instance = p_form.save(commit=False)
                        form_instance.profile = Profile.objects.get(user=request.user)
                        form_instance.dev_user_str = p_form.cleaned_data["dev_user_str"]
                        form_instance.save()
                else:
                    FavoriteGames.objects.filter(
                        profile_id=request.user.profile.id
                    ).filter(
                        dev_user_str=request.POST.get('dev_user_str')
                    ).delete()

            fav_game_check = list(FavoriteGames.objects.filter(profile_id=request.user.profile.id).values())
            devs_in_favs = [fav_game_check[i]['dev_user_str'] for i in range(len(fav_game_check))]

            dev_game_check_list = []

            for j, i in enumerate(dev_slug):
                if i in devs_in_favs:
                    dev_game_check_list.append('yes')
                else:
                    dev_game_check_list.append('no')

        else:
            dev_game_check_list = ""

        dev_list_name = sorted(list(zip_longest(dev_name, dev_img_address, dev_slug, dev_game_check_list, dev_order)),
                               key=lambda lowercase: lowercase[0].lower())

        dev_list_pop = sorted(list(zip_longest(dev_name, dev_img_address, dev_slug, dev_game_check_list, dev_order)),
                              key=lambda dev_order_list: dev_order_list[4])
        cache_key = "test_cache_key"

        if cache.get(cache_key) is not None:
            paginator_for_class_1 = Paginator(cache.get(cache_key), 48)
        else:
            cache.set(
                cache_key,
                dev_list_pop,
                60 * 60 * 4,
            )

        page = request.GET.get('page', 1)
        paginator2 = Paginator(dev_list_pop, 50)

        try:
            numbers = paginator2.page(page)
        except PageNotAnInteger:
            numbers = paginator2.page(1)
        except EmptyPage:
            numbers = paginator2.page(paginator2.num_pages)

        context = {'numbers': numbers}

        if request.method == "POST":
            return redirect("/my_favorites")
        else:
            return render(request, "homepage/dev_user.html", context)
    else:
        dev_query_results_init = TaskResult.objects.filter(task_name='homepage.tasks.rawg_fetch_dev')
        dev_query_results = json.loads(dev_query_results_init.values()[0]['result'])
        slug_index1 = [dev_query_results][0][0].index(slug)
        dev_list = [dev_query_results[0][slug_index1]]
        slugs_per_dev_list = dev_query_results[1][slug_index1]
        names_per_dev_list = dev_query_results[2][slug_index1]
        ratings_per_dev_list = dev_query_results[3][slug_index1]
        background_img_per_dev_list = dev_query_results[4][slug_index1]
        released_per_dev_list = dev_query_results[5][slug_index1]
        full_clip_per_dev_list = dev_query_results[6][slug_index1]
        ratings_count_per_dev_list = dev_query_results[7][slug_index1]

        dev_game_data = sorted(list(zip_longest(dev_list, slugs_per_dev_list, names_per_dev_list,
                                                ratings_per_dev_list, background_img_per_dev_list,
                                                released_per_dev_list,
                                                full_clip_per_dev_list, ratings_count_per_dev_list)),
                               key=lambda sort: sort[7], reverse=True)

        dev_game_data2 = []

        for i in range(len(dev_game_data)):
            try:
                if dev_game_data[i][4] is not None:
                    dev_game_data2.append(dev_game_data[i])
            except IndexError:
                pass

        page = request.GET.get('page', 1)
        paginator2 = Paginator(dev_game_data2, 20)

        try:
            numbers = paginator2.page(page)
        except PageNotAnInteger:
            numbers = paginator2.page(1)
        except EmptyPage:
            numbers = paginator2.page(paginator2.num_pages)

        if len(list(TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_dev').values())) == 1:
            google_query_results = json.loads(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_dev'
            ).values()[0]['result'])
        else:
            task_id_dev = list(TaskResult.objects.filter(
                task_name='homepage.tasks.google_fetch_dev'
            ).values())[1]['task_id']

            google_query_results = json.loads(TaskResult.objects.filter(
                task_id=task_id_dev
            ).values()[0]['result'])

        dev_name_list = list(Dev.objects.all().values_list('dev_name', flat=True))
        dev_slug_list = list(Dev.objects.all().values_list('dev_slug', flat=True))
        dev_slug_index = dev_slug_list.index(slug)
        dev_name_for_site = dev_name_list[dev_slug_index]
        google_search_results = [google_query_results[i] if google_query_results[i][6] == slug else 'none'
                                 for i in range(len(google_query_results))]

        google_search_results2 = []

        for i in range(len(google_search_results)):
            try:
                if google_search_results[i] != 'none':
                    google_search_results2.append(google_search_results[i])
            except IndexError:
                pass

        context = {
            'numbers': numbers,
            'google_search_results': google_search_results2,
            'dev_name_for_site': dev_name_for_site
        }

        return render(request, "homepage/dev_iter.html", context)


def about(request):
    return render(request, 'homepage/about.html')


def background(request):
    return render(request, 'homepage/background.html')
