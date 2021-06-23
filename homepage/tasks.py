import asyncio
import itertools
import math
import re
import sys
import time
from datetime import datetime
from itertools import zip_longest
import httpx
import nltk
import numpy as np
import pycld2
from asgiref.sync import sync_to_async
from celery import Celery
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from dateutil.relativedelta import relativedelta
from django_celery_results.models import TaskResult
import homepage.apivalues as api
from homepage.models import Dev, Google

app = Celery()


class AsyncFetchApi:
    """Asynchronously fetch data using Google and RAWG APIs."""
    def __init__(
            self,
            api_fetch_bool=False,
            database_query_bool=False,
            google_dev_query=False,
            google_games_query=False,
            google_dev_news1=False,
            google_dev_news2=False,
            google_dev_news3=False,
            google_dev_news4=False,
            google_dev_news5=False,
            google_query="",
            user_request="",
            fetch_dev_games=False,
            fetch_pop_games=False,
            fetch_upcm_games=False,
            max_page=False,
            google_api_key="",
            rawg_key="",
            cx1="",
            cx2="",
            cx3="",
            cx4="",
            cx5="",
            min_dev_for_google=0,
            max_dev_for_google=0,
    ):
        self.api_fetch_bool = api_fetch_bool
        self.database_query_bool = database_query_bool
        self.google_dev_query = google_dev_query
        self.google_games_query = google_games_query
        self.google_dev_news1 = google_dev_news1
        self.google_dev_news2 = google_dev_news2
        self.google_dev_news3 = google_dev_news3
        self.google_dev_news4 = google_dev_news4
        self.google_dev_news5 = google_dev_news5
        self.google_query = google_query
        self.user_request = user_request
        self.fetch_dev_games = fetch_dev_games
        self.fetch_pop_games = fetch_pop_games
        self.fetch_upcm_games = fetch_upcm_games
        self.max_page = max_page
        self.google_api_key = google_api_key
        self.rawg_key = rawg_key
        self.cx1 = cx1
        self.cx2 = cx2
        self.cx3 = cx3
        self.cx4 = cx4
        self.cx5 = cx5
        self.min_dev_for_google = min_dev_for_google
        self.max_dev_for_google = max_dev_for_google

    @sync_to_async
    def database_fetches(self):
        """
        Retrieve entries from database models for fetching.

        :return: tuple consisting of lists of Google queries and query iterators or a list of RAWG developer names.
        """
        if self.google_dev_query or self.google_games_query:
            range_min = self.min_dev_for_google
            range_max = self.max_dev_for_google

            if self.google_dev_query:
                return [str(Dev.objects.all().values()[i]['google_query'])
                        for i in range(len(Dev.objects.all()))][range_min:range_max], \
                       [Dev.objects.all().values()[i]['dev_slug']
                        for i in range(len(Dev.objects.all()))][range_min:range_max]


            elif self.google_games_query:
                if range_min == 'min' and range_max == 'all':
                    range_min = 0
                    range_max = len([str(Google.objects.all().values()[i]['g_query'])
                                     for i in range(len(Google.objects.all()))]) + 1

                return [str(Google.objects.all().values()[i]['g_query'])
                        for i in range(len(Google.objects.all()))][range_min:range_max], \
                       [Google.objects.all().values()[i]['query_iter']
                        for i in range(len(Google.objects.all()))][range_min:range_max]


        if self.fetch_dev_games:
            return [Dev.objects.all().values()[i]['dev_slug'] for i in range(len(Dev.objects.all()))]

    
    async def get_api_urls(self):
        """
        Prepare Google or RAWG URLs for asynchronous fetching.

        :return: list of urls for fetching
        """
        
        if self.google_dev_query or self.google_games_query:
            cx_broad1 = self.cx1
            cx_broad2 = self.cx2
            cx_broad3 = self.cx3
            cx_broad4 = self.cx4
            cx_broad5 = self.cx5

            if self.google_dev_query or self.google_games_query:
                google_query = await self.database_fetches()
                # Proprietary

        
        if self.fetch_dev_games:
            dev_slugs = await self.database_fetches()
            # Proprietary

        if self.api_fetch_bool:
            # Proprietary

        if self.database_query_bool:
            # Proprietary

    
    async def http_response_async(self):
        """
        Asynchronously fetch from Google and RAWG APIs. If max_page = True, then maximum page of RAWG API results will
        be returned.
        
        :return: list of fetched results or max page of RAWG API results
        """

        async with httpx.AsyncClient() as client:
            if self.google_dev_query or self.google_games_query:
                dev_urls = await self.get_api_urls()

                google_dev_query_responses = await asyncio.gather(
                    *[client.get(url) for url in google_dev_query_urls]
                )

                # Additional code functionality proprietary

            elif self.fetch_dev_games:
                dev_urls = await self.get_api_urls()

                dev_responses = await asyncio.gather(
                    *[client.get(url) for url in dev_urls]

                )

                # Additional code functionality proprietary

                if self.max_page:
                    # Proprietary

            else:
                if self.fetch_pop_games or self.fetch_upcm_games:
                    def get_yr_mo_d(yr_delta=0, mo_delta=0, d_delta=0):
                        today = datetime.today()
                        date_mod = str(
                            datetime(today.year + yr_delta, today.month + mo_delta, today.day + d_delta).date()
                        )
                        return date_mod

                    current_dt = get_yr_mo_d()
                    month_ahead = get_yr_mo_d(mo_delta=1)
                    year_ahead_5 = get_yr_mo_d(yr_delta=5)
                    year_ago = get_yr_mo_d(yr_delta=-12)

                    fetch_game_urls = await asyncio.gather(
                        *[client.get(url) for url in game_urls]
                    )

                    # Additional code functionality proprietary

    async def get_api_urls_w_max_page(self):
        """
        Prepare RAWG URLs for fetching up to max page of results.
        
        :return: list of urls
        """
        max_pages = await self.http_response_async()
        dev_slugs = await self.database_fetches()

        dev_slug_list = []

        for i in dev_slugs:
            i = [i]
            dev_slug_list.append(i)

        max_pages_list_init = [range(x) for x in max_pages]

        max_pages_list = [[x + 1 for x in max_pages_list_init[i]] for i in range(len(max_pages_list_init))]

        list_combined = list(zip(dev_slug_list, max_pages_list))

        dev_slug_list_final = []

        for p in range(len(max_pages_list)):
            for j in list_combined[p][1]:
                for i in list_combined[p][0]:
            # Proprietary

        return dev_slug_list_final

    async def http_response_async_max_page(self):
        """
        Fetch from RAWG API up to max page of query.
        
        :return: list of fetched results along with developer or publisher name associated with each result 
        """

        api_urls = await self.get_api_urls_w_max_page()

        async with httpx.AsyncClient() as client:
            if self.fetch_dev_games:
                fetch_to_max_age = await asyncio.gather(
                    *[client.get(url) for url in api_urls]

                )
            # Additional code functionality proprietary

        devs_or_pubs = [re.search('developers=(.*)&', api_urls[i]).group(1)
                        if type(re.search('developers=(.*)&', api_urls[i])) is not type(None)
                        else re.search('publishers=(.*)&', api_urls[i]).group(1)
                        for i in range(len(api_urls))]

        return list(zip(devs_or_pubs, fetch_to_max_age))


def google_function(i_api_init, g_dev=False, g_query=False):
    """
    Asynchronously fetch Google results.
    
    :param i_api_init: initial index of API to use for fetching 
    :param g_dev: fetch consists of results for game developer news
    :param g_query: fetch consists of results for general gaming news  
    """
    if g_dev:
        g_dev_length = len(list(Dev.objects.all()))
        g_dev_iter = math.ceil(g_dev_length / 5)
    elif g_query:
        g_query_length = len(list(Google.objects.all()))
        g_query_iter = math.ceil(g_query_length / 1)
    else:
        sys.exit("Google class not specified (0).")

    def google_article_fetch_concurrent(api_key_def,
                                        cx1_def,
                                        cx2_def,
                                        cx3_def,
                                        cx4_def,
                                        cx5_def,
                                        min_dev_def,
                                        max_dev_def,
                                        g_dev_def=g_dev,
                                        g_query_def=g_query):
        if g_dev_def:
            g_fetch1 = asyncio.run(AsyncFetchApi(google_dev_query=True,
                                                 google_dev_news1=True,
                                                 google_api_key=api_key_def,
                                                 cx1=cx1_def,
                                                 cx2=cx2_def,
                                                 cx3=cx3_def,
                                                 cx4=cx4_def,
                                                 cx5=cx5_def,
                                                 min_dev_for_google=min_dev_def,
                                                 max_dev_for_google=max_dev_def).http_response_async())

            # Additional code functionality proprietary

        elif g_query_def:
            
            g_fetch1 = asyncio.run(AsyncFetchApi(google_games_query=True,
                                                 google_dev_news1=True,
                                                 google_api_key=api_key_def,
                                                 cx1=cx1_def,
                                                 cx2=cx2_def,
                                                 cx3=cx3_def,
                                                 cx4=cx4_def,
                                                 cx5=cx5_def,
                                                 min_dev_for_google=min_dev_def,
                                                 max_dev_for_google=max_dev_def).http_response_async())

            # Additional code functionality proprietary

    
    i_iter_init = 0
    google_db_query_results_init = []

    if g_dev:
        
        for i in range(0, 5):
            min_dev_iter = i_iter_init
            i_iter_init += g_dev_iter
            if i_iter_init < g_dev_length:
                max_dev_iter = i_iter_init
            else:
                max_dev_iter = g_dev_length + 1
            api_key = api.api[i_api_init]

            cx1, cx2, cx3, cx4, cx5 = [j for j in api.cx]

            google_db_query_results_init.append(google_article_fetch_concurrent(api_key_def=api_key,
                                                                                cx1_def=cx1,
                                                                                cx2_def=cx2,
                                                                                cx3_def=cx3,
                                                                                cx4_def=cx4,
                                                                                cx5_def=cx5,
                                                                                min_dev_def=min_dev_iter,
                                                                                max_dev_def=max_dev_iter,
                                                                                g_dev_def=g_dev,
                                                                                g_query_def=g_query))

    elif g_query:
        
        for i in range(0, 1):
            min_dev_iter = i_iter_init
            i_iter_init += g_query_iter
            if i_iter_init < g_query_length:
                max_dev_iter = i_iter_init
            else:
                max_dev_iter = g_query_length + 1
            api_key = api.api[i_api_init]

            cx1, cx2, cx3, cx4, cx5 = [j for j in api.cx]

            google_db_query_results_init.append(google_article_fetch_concurrent(api_key_def=api_key,
                                                                                cx1_def=cx1,
                                                                                cx2_def=cx2,
                                                                                cx3_def=cx3,
                                                                                cx4_def=cx4,
                                                                                cx5_def=cx5,
                                                                                min_dev_def=min_dev_iter,
                                                                                max_dev_def=max_dev_iter,
                                                                                g_dev_def=g_dev,
                                                                                g_query_def=g_query))
    else:
        sys.exit("Google class not specified (2).")

    
    if g_dev:
        unique_google_queries = [i['dev_slug'] for i in list(Dev.objects.all().values())]
    elif g_query:
        unique_google_queries = [i['query_iter'] for i in list(Google.objects.all().values())]
    else:
        sys.exit("Google class not specified (3).")

    
    combined_query = list(itertools.chain.from_iterable(
        [list(itertools.chain.from_iterable(
            [i for i in google_db_query_results_init[j]]))
            for j in range(len(google_db_query_results_init))]))

    # Removing page hits that did not yield results
    google_db_query_results = []

    for i in range(len(combined_query)):
        if len(combined_query[i][1].keys()) == 6:
            google_db_query_results.append(combined_query[i])

    # Grepping fetch hit results
    google_hits_tot = [(i[0], i[1]['items']) for i in google_db_query_results]

    # Sorting results by Google search queries used in asynchronous fetching
    google_hits_tot_slug_sorted = [(j, [i[1] for i in google_hits_tot if i[0] == j]) for j in unique_google_queries]

    # Linking Google search queries to fetch results
    query_hit_count_sum = [(unique_google_queries[i], sum([len(google_hits_tot_slug_sorted[i][1][j])
                                                           for j in range(len(google_hits_tot_slug_sorted[i][1]))]))
                           for i in range(len(google_hits_tot_slug_sorted))]

    # Handles errors by outputting 'none' if error encountered
    def catch(func, handle=lambda e: 'none', *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return handle(e)

    # Preparing to retrieve results in json format
    prep_for_results = [list(itertools.chain.from_iterable([google_hits_tot_slug_sorted[j][1][i]
                                                            for i in range(len(google_hits_tot_slug_sorted[j][1]))]))
                        for j in range(len(google_hits_tot_slug_sorted))]

    # Retrieving fetch titles
    title_per_google_fetch = list(itertools.chain.from_iterable([[catch(lambda: prep_for_results[i][j]['title'])
                                                                  for j in range(len(prep_for_results[i]))]
                                                                 for i in range(len(prep_for_results))]))
    # Retrieving fetch links
    link_combined = list(itertools.chain.from_iterable([[catch(lambda: prep_for_results[i][j]['link'])
                                                         for j in range(len(prep_for_results[i]))]
                                                        for i in range(len(prep_for_results))]))

    # Removing link url schemes and returning links composed of subdomain as well as second- and top-level domains
    link_com_init = [re.match('h.*\..{,5}/{1}', link_combined[i]).group(0)
                     if type(re.match('h.*\..{,5}/{1}', link_combined[i]))
                        != type(None) else 'none'
                     for i in range(len(link_combined))]

    link_filter_init = [i if i.count('/') == 3 else 'none' for i in link_com_init]

    link_filter_sub = [re.sub('https://www\\.', '', link_filter_init[i]) if 'www.' in link_filter_init[i]
                       else re.sub('https://', '', link_filter_init[i]) for i in range(len(link_filter_init))]

    link_com = [i.replace('/', '') for i in link_filter_sub]

    link_combined_filtered = [link_combined[i] if link_filter_init[i] != 'none' else 'none'
                              for i in range(len(link_combined))]

    link_per_google_fetch = [i.replace('http://', 'https://') for i in link_combined_filtered]

    # Retrieving fetch snippets
    snippet_per_google_fetch = list(itertools.chain.from_iterable([[catch(lambda: prep_for_results[i][j]['snippet'])
                                                                    for j in range(len(prep_for_results[i]))]
                                                                   for i in range(len(prep_for_results))]))

    # Retrieving fetch thumbnails
    cse_thumbnail_combined = list(itertools.chain.from_iterable(
        [[catch(lambda: prep_for_results[i][j]['pagemap']['cse_thumbnail'][0]['src'])
          for j in range(len(prep_for_results[i]))]
         for i in range(len(prep_for_results))]))

    cse_thumbnail_per_google_fetch = [i.replace('http://', 'https://') for i in cse_thumbnail_combined]

    # Retrieving fetch og images
    og_img_combined = list(itertools.chain.from_iterable(
        [[catch(lambda: prep_for_results[i][j]['pagemap']['metatags'][0]['og:image'])
          for j in range(len(prep_for_results[i]))]
         for i in range(len(prep_for_results))]))

    og_img_per_google_fetch = [i.replace('http://', 'https://') for i in og_img_combined]

    # Retrieving dates from snippets
    date_extract_init = [re.match('([A-Za-z0-9, ]*)', snippet_per_google_fetch[i]).group(0)
                         if type(re.match('([A-Za-z0-9, ]*) \\.\\.\\.', snippet_per_google_fetch[i]))
                            is not type(None) else 'none' for i in range(len(snippet_per_google_fetch))]

    date_extract_init = [re.sub(' $', '', date_extract_init[i]) for i in range(len(snippet_per_google_fetch))]

    # Converting extracted dates to datetime objects
    date_extract = []

    for i in date_extract_init:
        try:
            if 'ago' in i:
                value, unit = re.search(r'(\d+) (\w+)', i).groups()
                if not unit.endswith('s'):
                    unit += 's'
                delta = relativedelta(**{unit: int(value)})
                date_fin = datetime.today() - delta
                date_extract.append(date_fin)
            elif i == 'none':
                date_extract.append('none')
            elif bool(re.match('[0-9]{1,2} [A-Za-z]', i)):
                datetime_strip = datetime.strptime(i, '%d %b %Y')
                date_extract.append(datetime_strip)
            else:
                datetime_strip = datetime.strptime(i, '%b %d, %Y')
                date_extract.append(datetime_strip)
        except ValueError:
            date_extract.append('none')

    # Necessary to now directly link compiled fetch results to unique Google queries that spawned results (quantities of
    # results may vary per Google query)

    if g_dev:
        # Preparing developer db entries for linking to Google fetched results
        dev_name_for_site_init = list(Dev.objects.all().values_list('dev_name', flat=True))
        dev_slug_for_site_init = list(Dev.objects.all().values_list('dev_slug', flat=True))
        dev_img_for_site_init = list(Dev.objects.all().values_list('dev_image_address', flat=True))
        dev_for_site = [(dev_name_for_site_init[i], dev_slug_for_site_init[i], dev_img_for_site_init[i]) for
                        i in range(len(dev_name_for_site_init))]
        combine_index = [dev_slug_for_site_init.index(unique_google_queries[i])
                         for i in range(len(unique_google_queries))]
        combine_dev_props = [dev_for_site[i] for i in combine_index]

        dev_name_for_site = [i[0] for i in combine_dev_props]
        dev_slug_for_site = [i[1] for i in combine_dev_props]
        dev_img_for_site = [i[2] for i in combine_dev_props]

    elif g_query:
        # Preparing general game query db entries for linking to Google fetched results
        g_id_init = list(Google.objects.all().values_list('query_iter', flat=True))
        g_query_init = list(Google.objects.all().values_list('g_query', flat=True))

        g_id_and_query = [(g_id_init[i], g_query_init[i]) for
                          i in range(len(g_id_init))]
        combine_index = [g_id_init.index(unique_google_queries[i])
                         for i in range(len(unique_google_queries))]
        combine_dev_props = [g_id_and_query[i] for i in combine_index]

        g_id = [i[0] for i in combine_dev_props]
        g_query_fin = [i[1] for i in combine_dev_props]

    else:
        sys.exit("Google class is not specified (4).")

    # Summing total query hits per query
    hit_query_total = [(query_hit_count_sum[j][0], sum([i if type(i) is int else 0
                                                        for i in query_hit_count_sum[j]]))
                       for j in range(len(query_hit_count_sum))]

    # Logic to yield list that will contain indexes for query results
    query_entry_init = [i[1] for i in hit_query_total]

    query_entry = []

    for i in range(len(query_entry_init)):
        if len(query_entry) == 0:
            query_entry.append(query_entry_init[i])
        else:
            query_entry.append(query_entry_init[i] + query_entry[i - 1])

    # Defining function to link fetched results to originating db queries
    def hit_index_return(int_check):
        try:
            if int(int_check) < int(query_entry[0]):
                return 0
            else:
                max_limit = [query_entry[i] for i in range(len(query_entry))
                             if query_entry[i] > int_check][:1]
                return query_entry.index(max_limit[0])
        except IndexError:
            return len(query_entry) - 1

    if g_dev:
        # Linking originating db queries to developer news fetched results
        dev_name_query_link = []
        dev_slug_query_link = []
        dev_img_query_link = []

        try:
            for i in range(len(cse_thumbnail_per_google_fetch)):
                index_input = hit_index_return(i)
                dev_name_query_link.append(dev_name_for_site[index_input])
                dev_slug_query_link.append(dev_slug_for_site[index_input])
                dev_img_query_link.append(dev_img_for_site[index_input])
        except IndexError:
            pass

    elif g_query:
        # Linking originating db queries to general game news fetched results
        g_id_query_link = []
        g_query_link = []

        try:
            for i in range(len(cse_thumbnail_per_google_fetch)):
                index_input = hit_index_return(i)
                g_id_query_link.append(g_id[index_input])
                g_query_link.append(g_query_fin[index_input])
        except IndexError:
            pass
    else:
        sys.exit("Google class not specified (5).")

    if g_dev:
        # Determining if thumbnails exist and, if not, replacing entries with static img address per developer
        cse_thumbnail2 = [
            (cse_thumbnail_per_google_fetch[i], 'yes') if cse_thumbnail_per_google_fetch[i] != 'none' else
            (str(dev_img_query_link[i]), 'no_dev')
            for i in range(len(cse_thumbnail_per_google_fetch))
        ]

    elif g_query:
        # Determining if thumbnails exist and, if not, replacing entries with static img address of logo. Also included
        # in tuple is designator indicating if thumbnail entry was retained or replaced.
        cse_thumbnail2 = [
            (cse_thumbnail_per_google_fetch[i], 'yes') if cse_thumbnail_per_google_fetch[i] != 'none' else
            ('logo_default.svg', 'no_query')
            for i in range(len(cse_thumbnail_per_google_fetch))
        ]
    else:
        sys.exit("Google class not specified (6).")

    # Retrieving thumbnails / static img addresses
    cse_thumbnail3 = [cse_thumbnail2[i][0] for i in range(len(cse_thumbnail2))]

    # Retrieving second tuple element specifying if thumbnail entry was retained or replaced
    cse_thumbnail_for_ref = [cse_thumbnail2[i][1] for i in range(len(cse_thumbnail2))]

    if g_dev:
        # Compiling fetched and processed developer news results
        google_search_results = list(
            zip_longest(title_per_google_fetch, link_per_google_fetch, snippet_per_google_fetch,
                        cse_thumbnail3, cse_thumbnail_for_ref, dev_name_query_link, dev_slug_query_link,
                        link_com, date_extract, og_img_per_google_fetch))

    elif g_query:
        # Compiling fetched and processed general game news results
        google_search_results = list(
            zip_longest(title_per_google_fetch, link_per_google_fetch, snippet_per_google_fetch,
                        cse_thumbnail3, cse_thumbnail_for_ref, g_id_query_link, g_query_fin, link_com,
                        date_extract, og_img_per_google_fetch))
    else:
        sys.exit("Google class not specified (7).")

    # Now fetched and processed results with be additionally filtered to obtain the best quality results, which is
    # defined as unique results that link directly to original articles

    # Retrieving snippet text (i.e., removing date from snippet)
    snippet_extract = []

    for i in range(len(snippet_per_google_fetch)):
        try:
            snippet_extract.append(re.search('[.]{3}.*', snippet_per_google_fetch[i]).group(0))
        except AttributeError:
            snippet_extract.append(snippet_per_google_fetch[i])

    # Filtering fetched and processed news results to yield hits written in the English language that have a high
    # probability of linking directly to original articles
    google_search_results2 = []

    for i in range(len(snippet_per_google_fetch)):
        try:
            if pycld2.detect(snippet_extract[i])[2][0][0] == 'ENGLISH' \
                    and bool(re.search('-', link_per_google_fetch[i])) \
                    or bool(re.search('_', link_per_google_fetch[i])):
                google_search_results2.append(google_search_results[i])
        except IndexError:
            pass

    # Retrieving unique links from filtered Google results
    link_per_google_fetch2 = [i[1] for i in google_search_results2]

    link_count = [link_per_google_fetch2.count(link_per_google_fetch2[i]) for i in
                  range(len(link_per_google_fetch2))]

    link_zip = list(zip(link_per_google_fetch2, link_count))

    link_unique = [link_zip[i][0] if link_zip[i][1] == 1 else 'none' for i in
                   range(len(link_zip))]

    # Obtaining indices of non-unique links
    nonunique_indices_link = [i for i, x in enumerate(link_unique) if x == "none"]

    # Generating list containing fetched results where the link within the results is non-unique and the first
    # instance
    nonunique_check_link = []
    nonunique_entries_nonrepeat_link = []

    for i in nonunique_indices_link:
        nonunique_check_link.append(link_per_google_fetch2[i])
        count_inst = nonunique_check_link.count(link_per_google_fetch2[i])
        if count_inst == 1:
            nonunique_entries_nonrepeat_link.append(google_search_results2[i])

    # Additionally filtering fetched and processed results to contain hits with only unique links
    google_search_results3_init = []

    for i in range(len(link_unique)):
        try:
            if link_unique[i] != 'none':
                google_search_results3_init.append(google_search_results2[i])
        except IndexError:
            pass

    # Appending list containing fetched results where the link within the results is non-unique and the first instance 
    # to list containing filtered fetched results with only unique links
    google_search_results3_mid = google_search_results3_init + nonunique_entries_nonrepeat_link

    # Retrieving unique links from filtered Google results
    title_instances = [i[0] for i in google_search_results3_mid]

    title_count = [title_instances.count(title_instances[i]) for i in range(len(title_instances))]

    title_zip = list(zip(title_instances, title_count))

    title_unique = [title_zip[i][0] if title_zip[i][1] == 1 else 'none' for i in range(len(title_zip))]

    # Obtaining indices of non-unique links
    nonunique_indices_title = [i for i, x in enumerate(title_unique) if x == "none"]

    nonunique_check_title = []
    nonunique_entries_nonrepeat_title = []

    # Generating list containing fetched results where the title within the results is non-unique and the first
    # instance
    for i in nonunique_indices_title:
        nonunique_check_title.append(title_instances[i])
        count_inst = nonunique_check_title.count(title_instances[i])
        if count_inst == 1:
            nonunique_entries_nonrepeat_title.append(google_search_results3_mid[i])

    # Additionally filtering fetched and processed results to contain hits with only unique titles
    google_search_results3_mid_2 = []

    for i in range(len(title_unique)):
        try:
            if title_unique[i] != 'none':
                google_search_results3_mid_2.append(google_search_results3_mid[i])
        except IndexError:
            pass

    # Appending list containing fetched results where the title within the results is non-unique and the first instance 
    # to list containing filtered fetched results with only unique titles
    google_search_results3 = google_search_results3_mid_2 + nonunique_entries_nonrepeat_title

    # Retrieving snippets from fetched, processed, and filtered Google results
    snippet_filtered = [i[2] for i in google_search_results3]

    # Retrieving filtered snippet text (i.e., removing date from snippet)
    snippet_extract_filtered = []

    for i in range(len(snippet_filtered)):
        try:
            snippet_extract_filtered.append(re.search('[.]{3}.*', snippet_filtered[i]).group(0))
        except AttributeError:
            snippet_extract_filtered.append(snippet_filtered[i])

    # Implementing functionality to determine if snippet consists of complete sentences, which will yield the highest
    # quality fetched results as previously defined.
    tokens = [nltk.word_tokenize(i) for i in snippet_extract_filtered]

    time.sleep(4)
    pos_tags = [nltk.pos_tag(i) for i in tokens]
    time.sleep(4)
    tags = [[pos_tags[j][i][1] for i in range(len(pos_tags[j]))] for j in range(len(pos_tags))]

    tags_count = [([(':', tags[i].count(':')), ('NN', tags[i].count('NN')), ('NNP', tags[i].count('NNP')),
                    ('NNPS', tags[i].count('NNPS')), ('NNS', tags[i].count('NNS')),
                    ('RB', tags[i].count('RB')),
                    ('RBR', tags[i].count('RBR')), ('RBS', tags[i].count('RBS')),
                    ('RP', tags[i].count('RP')),
                    ('VB', tags[i].count('VB')), ('VBD', tags[i].count('VBD')),
                    ('VBG', tags[i].count('VBG')),
                    ('VBN', tags[i].count('VBN')), ('VBP', tags[i].count('VBP')),
                    ('VBZ', tags[i].count('VBZ'))], snippet_extract_filtered[i]) for i in range(len(tags))]

    colon_sentence = [[tags_count[j][0][i][1] for i in range(len(tags_count[0][0]))][:1][0]
                      for j in range(len(tags_count))]
    nnp_sentence = [[tags_count[j][0][i][1] for i in range(len(tags_count[0][0]))][2:3][0]
                    for j in range(len(tags_count))]
    pos_rb_vb_sentence = [sum([tags_count[j][0][i][1] for i in range(len(tags_count[0][0]))][5:])
                          for j in range(len(tags_count))]

    tags_count_filter2 = [snippet_filtered[i] if colon_sentence[i] < 6 and nnp_sentence[i] < 10 and
                                                 pos_rb_vb_sentence[i] >= 2 else 'none'
                          for i in range(len(tags_count))]

    # Filtering fetched and processed results to contain only snippets consisting of complete sentences
    google_search_results4 = []

    for i in range(len(tags_count_filter2)):
        try:
            if tags_count_filter2[i] != 'none':
                google_search_results4.append(google_search_results3[i])
        except IndexError:
            pass

    # Retrieving snippets from fetched, processed, and filtered results
    snippet_filtered2 = [i[2] for i in google_search_results4]

    # Removing instances of '...' from snippets
    snippet_extract_filtered2 = []

    for i in range(len(snippet_filtered2)):
        try:
            snippet_extract_filtered2.append(
                re.search(
                    '[.]{3}.*', snippet_filtered2[i], re.DOTALL
                ).group(0).replace('... ...', '...').replace('...', '')
            )
        except AttributeError:
            snippet_extract_filtered2.append(snippet_filtered2[i].replace('... ...', '...').replace('...', ''))

    # Replace previous snippets containing '...' with snippet elements in which text has remained the same but
    # instances of '...' have been removed
    google_search_results5 = [[google_search_results4[i][j] if j != 2 else snippet_extract_filtered2[i]
                               for j in range(len(google_search_results4[i]))] for i in
                              range(len(google_search_results4))]

    # Remove all fetched results that are older than 1 year from current time
    google_search_results6_init = []

    for i in google_search_results5:
        if bool(isinstance(i[8], datetime)):
            google_search_results6_init.append(i)

    delta_t_1_yr = [(datetime.today() - google_search_results6_init[i][8])
                    < (datetime.today() - datetime(year=datetime.today().year - 1, month=datetime.today().month,
                                                   day=datetime.today().day))
                    for i in range(len(google_search_results6_init))]

    google_search_results6 = [google_search_results6_init[i]
                              for i in range(len(google_search_results6_init)) if delta_t_1_yr[i] is not False]

    # Delete previous Google fetch tasks depending on instance of task run
    if g_dev:
        TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_dev').delete()
    elif g_query:
        TaskResult.objects.filter(task_name='homepage.tasks.google_fetch_query').delete()
    else:
        sys.exit("Google class not specified (9).")

    return sorted(google_search_results6, key=lambda sort: sort[8], reverse=True)


@shared_task(time_limit=800, soft_time_limit=500)
def google_fetch_dev(api_input):
    """
    Runs function to fetch Google results for queries pertaining to latest developer news.
    
    :return: results of asynchronous fetch
    """
    try:
        return google_function(i_api_init=api_input, g_dev=True)

    except SoftTimeLimitExceeded as e:
        print(e, type(e))


@shared_task(time_limit=800, soft_time_limit=500)
def google_fetch_query(api_input):
    """
    Runs function to fetch Google results for queries pertaining to latest game news.

    :return: results of asynchronous fetch
    """
    try:
        return google_function(i_api_init=api_input, g_query=True)

    except SoftTimeLimitExceeded as e:
        print(e, type(e))


@shared_task(time_limit=120, soft_time_limit=90)
def rawg_fetch(key, rawg_dev=False, rawg_pop=False, rawg_upcm=False):
    """
    Fetch RAWG results for developer games, popular games, and upcoming games
    
    :param rawg_dev: fetch consists of results for RAWG developers
    :param rawg_pop: fetch consists of results for RAWG popular games
    :param rawg_upcm: fetch consists of results for RAWG upcoming games
    :return: list of fetched results
    """
    try:
        if rawg_dev:
            rawg_db_query_results = asyncio.run(
                AsyncFetchApi(rawg_key=key, fetch_dev_games=True, max_page=True).http_response_async_max_page())
        elif rawg_pop:
            rawg_db_query_results = asyncio.run(AsyncFetchApi(rawg_key=key, fetch_pop_games=True).http_response_async())
        elif rawg_upcm:
            rawg_db_query_results = asyncio.run(
                AsyncFetchApi(rawg_key=key, fetch_upcm_games=True).http_response_async())
        else:
            sys.exit("RAWG fetch type not specified (1).")

        # Handles errors by outputting 'none' if error encountered
        def catch(func, handle=lambda e: 'none', *args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return handle(e)

        if rawg_dev:
            # Obtaining developer games from asynchronous RAWG fetch
            game_per_fetch = [rawg_db_query_results[i][0] for i in range(len(rawg_db_query_results))]

            # Generating unique list of developer games
            unique_games = np.unique(np.array(game_per_fetch))

            # Combining RAWG fetch into one consolidated list
            combined_query = list(itertools.chain.from_iterable(rawg_db_query_results))

            # Linking unique instances of games to RAWG fetch results for each game
            query_results = [[combined_query[i + 1]['results'] for i in range(len(combined_query)) if
                              combined_query[i] == unique_games[j]] for j in range(len(unique_games))]

            # Defining function to retrieve RAWG fetch results in json format
            def dev_game_query_search(query):
                return [[item for sublist in [[[catch(lambda: query_results[k][j][i][query]) for i in
                                                range(len(query_results[k][j]))] for j in
                                               range(len(query_results[k]))] for k in
                                              range(len(unique_games))][n]
                         for item in sublist] for n in range(len(unique_games))]

            # Retrieving json results from RAWG fetch
            slugs_per_dev_list = dev_game_query_search('slug')
            names_per_dev_list = dev_game_query_search('name')
            ratings_per_dev_list = dev_game_query_search('rating')
            background_img_per_dev_list = dev_game_query_search('background_image')
            released_per_dev_list = dev_game_query_search('released')
            full_clip_per_dev_list = [[item for sublist in
                                       [[[catch(lambda: query_results[k][j][i]['clip']['clips']['full'])
                                          for i in range(len(query_results[k][j]))] for j in
                                         range(len(query_results[k]))] for k in
                                        range(len(unique_games))][n]
                                       for item in sublist] for n in range(len(unique_games))]
            ratings_count_per_dev_list = dev_game_query_search('ratings_count')
            TaskResult.objects.filter(task_name='homepage.tasks.rawg_dev_game_db_creation').delete()

            return unique_games.tolist(), slugs_per_dev_list, names_per_dev_list, ratings_per_dev_list, \
                   background_img_per_dev_list, released_per_dev_list, full_clip_per_dev_list, \
                   ratings_count_per_dev_list

        elif rawg_pop or rawg_upcm:
            # Obtaining popular or upcoming games from asynchronous RAWG fetch
            db_combined_init = [rawg_db_query_results[i]['results'] for i in range(len(rawg_db_query_results))]
            db_combined = [j for i in db_combined_init for j in i]

            # Retrieving json results from RAWG fetch
            slugs_per_dev_list = [catch(lambda: db_combined[i]['slug']) for i in range(len(db_combined))]
            names_per_dev_list = [catch(lambda: db_combined[i]['name']) for i in range(len(db_combined))]
            ratings_per_dev_list = [catch(lambda: db_combined[i]['rating']) for i in range(len(db_combined))]
            background_img_per_dev_list = [catch(lambda: db_combined[i]['background_image'])
                                           for i in range(len(db_combined))]
            released_per_dev_list = [catch(lambda: db_combined[i]['released'])
                                     for i in range(len(db_combined))]
            to_play_dev_list = [catch(lambda: db_combined[i]['added_by_status']['toplay'])
                                for i in range(len(db_combined))]

            ratings_count_per_dev_list = [catch(lambda: db_combined[i]['ratings_count'])
                                          for i in range(len(db_combined))]
            TaskResult.objects.filter(task_name='homepage.tasks.rawg_dev_game_db_creation').delete()

            return slugs_per_dev_list, names_per_dev_list, ratings_per_dev_list, \
                   background_img_per_dev_list, released_per_dev_list, to_play_dev_list, \
                   ratings_count_per_dev_list
        else:
            sys.exit("RAWG fetch type not specified (2).")

    except SoftTimeLimitExceeded as e:
        print(e, type(e))


@shared_task(time_limit=120, soft_time_limit=90)
def rename_rawg_task(rawg_dev=False, rawg_pop=False, rawg_upcm=False):
    """
    Rename RAWG celery task so that task name indicates type of fetch run.

    :param rawg_dev: designates that fetch consisted of results for RAWG developers
    :param rawg_pop: designates that fetch consisted of results for RAWG popular games
    :param rawg_upcm: designates that fetch consisted of results for RAWG upcoming games
    """

    if TaskResult.objects.filter(task_name='homepage.tasks.rawg_fetch').values_list()[0][5] == 'SUCCESS' \
            and not TaskResult.objects.filter(
        task_name='homepage.tasks.rawg_fetch'
    ).values_list()[0][9] == 'null':
        try:
            if rawg_dev:
                upd_str = 'dev'
            elif rawg_pop:
                upd_str = 'pop'
            elif rawg_upcm:
                upd_str = 'upcm'
            else:
                sys.exit("RAWG db type not specified (1).")

            TaskResult.objects.filter(task_name=f'homepage.tasks.rawg_fetch_{upd_str}').delete()

            TaskResult.objects.filter(
                task_name='homepage.tasks.rawg_fetch'
            ).update(
                task_name=f'homepage.tasks.rawg_fetch_{upd_str}'
            )

            TaskResult.objects.filter(task_name='homepage.tasks.rename_rawg_task').delete()

        except SoftTimeLimitExceeded as e:
            print(e, type(e))


# Task concepts that may be populated in the future

@shared_task(time_limit=120, soft_time_limit=90)
def twitch_game_streaming_fetch():
    try:
        TaskResult.objects.filter(task_name='homepage.tasks.twitch_game_streaming_fetch').delete()
        return asyncio.run(AsyncFetchApi().http_response_async())
    except SoftTimeLimitExceeded as e:
        print(e, type(e))


@shared_task(time_limit=120, soft_time_limit=90)
def youtube_game_related_fetch():
    try:
        TaskResult.objects.filter(task_name='homepage.tasks.youtube_game_related_fetch').delete()
        return asyncio.run(AsyncFetchApi().http_response_async())
    except SoftTimeLimitExceeded as e:
        print(e, type(e))


@shared_task(time_limit=120, soft_time_limit=90)
def spotify_game_related_fetch():
    try:
        TaskResult.objects.filter(task_name='homepage.tasks.spotify_game_related_fetch').delete()
        return asyncio.run(AsyncFetchApi().http_response_async())
    except SoftTimeLimitExceeded as e:
        print(e, type(e))
