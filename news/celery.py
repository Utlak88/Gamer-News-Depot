import os
from celery import Celery
from news import settings
from celery.schedules import crontab
from homepage.apivalues import rawg_key

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

celery_app = Celery('news',
                    broker=settings.BROKER_URL,
                    )

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()

redbeat_redis_url = 'redis://localhost:6379/1'

celery_app.conf.timezone = 'US/Eastern'


def cron_schedule(g_dev_hr=5, g_dev_mi=0,
                  g_query_hr=6, g_query_mi=0,
                  rawg_dev_hr=0, rawg_dev_mi=0,
                  rawg_pop_hr=0, rawg_pop_mi=5,
                  rawg_upcm_hr=0, rawg_upcm_mi=10,
                  rawg_iter=1):

    def cron_24hr_clock(d_w, d_mo, mo, cron_mi=0, cron_hr=0, cron_iter=0, cron_multiplier=1) -> crontab:
        """
        Determines if crontabs for linked tasks (e.g., RAWG rename task after RAWG fetch task) will be run in the next
        hour or day. If so, hour and/or day will be adjusted accordingly.

        :return: task crontab with adjustments to hour and/or day if necessary
        """
        if cron_mi + cron_iter * cron_multiplier > 59 and cron_hr + 1 <= 23:
            return crontab(minute=cron_mi + cron_iter * cron_multiplier - 60, hour=cron_hr + 1, day_of_week=d_w,
                           day_of_month=d_mo, month_of_year=mo)
        elif cron_mi + cron_iter * cron_multiplier > 59 and cron_hr + 1 > 23:
            return crontab(minute=cron_mi + cron_iter * cron_multiplier - 60, hour=cron_hr + 1 - 24, day_of_week=d_w,
                           day_of_month=d_mo, month_of_year=mo)
        else:
            return crontab(minute=cron_mi + cron_iter * cron_multiplier, hour=cron_hr, day_of_week=d_w,
                           day_of_month=d_mo, month_of_year=mo)

    g_dev_fetch_cron1 = crontab(minute=g_dev_mi, hour=g_dev_hr, day_of_week='*', day_of_month='*',
                                month_of_year='*')

    g_dev_fetch_cron2 = crontab(minute=g_dev_mi, hour=g_dev_hr + 2, day_of_week='*', day_of_month='*',
                                month_of_year='*')

    g_dev_fetch_cron3 = crontab(minute=g_dev_mi, hour=g_dev_hr + 4, day_of_week='*', day_of_month='*',
                                month_of_year='*')

    g_dev_fetch_cron4 = crontab(minute=g_dev_mi, hour=g_dev_hr + 6, day_of_week='*', day_of_month='*',
                                month_of_year='*')

    g_dev_fetch_cron5 = crontab(minute=g_dev_mi, hour=g_dev_hr + 8, day_of_week='*', day_of_month='*',
                                month_of_year='*')

    g_dev_fetch_cron6 = crontab(minute=g_dev_mi, hour=g_dev_hr + 10, day_of_week='*', day_of_month='*',
                                month_of_year='*')

    g_dev_fetch_cron7 = crontab(minute=g_dev_mi, hour=g_dev_hr + 12, day_of_week='*', day_of_month='*',
                                month_of_year='*')

    g_dev_fetch_cron8 = crontab(minute=g_dev_mi, hour=g_dev_hr + 14, day_of_week='*', day_of_month='*',
                                month_of_year='*')

    g_dev_fetch_cron9 = crontab(minute=g_dev_mi, hour=g_dev_hr + 16, day_of_week='*', day_of_month='*',
                                month_of_year='*')

    g_dev_fetch_cron10 = crontab(minute=g_dev_mi, hour=g_dev_hr + 18, day_of_week='*', day_of_month='*',
                                 month_of_year='*')

    g_query_fetch_cron1 = crontab(minute=g_query_mi, hour=g_query_hr, day_of_week='*', day_of_month='*',
                                  month_of_year='*')

    g_query_fetch_cron2 = crontab(minute=g_query_mi, hour=g_query_hr + 2, day_of_week='*', day_of_month='*',
                                  month_of_year='*')

    g_query_fetch_cron3 = crontab(minute=g_query_mi, hour=g_query_hr + 4, day_of_week='*', day_of_month='*',
                                  month_of_year='*')

    g_query_fetch_cron4 = crontab(minute=g_query_mi, hour=g_query_hr + 6, day_of_week='*', day_of_month='*',
                                  month_of_year='*')

    g_query_fetch_cron5 = crontab(minute=g_query_mi, hour=g_query_hr + 8, day_of_week='*', day_of_month='*',
                                  month_of_year='*')

    g_query_fetch_cron6 = crontab(minute=g_query_mi, hour=g_query_hr + 10, day_of_week='*', day_of_month='*',
                                  month_of_year='*')

    g_query_fetch_cron7 = crontab(minute=g_query_mi, hour=g_query_hr + 12, day_of_week='*', day_of_month='*',
                                  month_of_year='*')

    g_query_fetch_cron8 = crontab(minute=g_query_mi, hour=g_query_hr + 14, day_of_week='*', day_of_month='*',
                                  month_of_year='*')

    g_query_fetch_cron9 = crontab(minute=g_query_mi, hour=g_query_hr + 16, day_of_week='*', day_of_month='*',
                                  month_of_year='*')

    g_query_fetch_cron10 = crontab(minute=g_query_mi, hour=0, day_of_week='*', day_of_month='*',
                                   month_of_year='*')

    rawg_fetch_dev_cron = crontab(minute=rawg_dev_mi, hour=rawg_dev_hr, day_of_week='*', day_of_month=1,
                                  month_of_year='*')

    rawg_fetch_pop_cron = crontab(minute=rawg_pop_mi, hour=rawg_pop_hr, day_of_week='*', day_of_month=1,
                                  month_of_year='*')

    rawg_fetch_upcm_cron = crontab(minute=rawg_upcm_mi, hour=rawg_upcm_hr, day_of_week='*', day_of_month=1,
                                   month_of_year='*')

    rename_rawg_dev_task_cron = cron_24hr_clock(d_w='*', d_mo=1, mo='*', cron_mi=rawg_dev_mi, cron_hr=rawg_dev_hr,
                                                cron_iter=rawg_iter, cron_multiplier=1)

    rename_rawg_pop_task_cron = cron_24hr_clock(d_w='*', d_mo=1, mo='*', cron_mi=rawg_pop_mi, cron_hr=rawg_pop_hr,
                                                cron_iter=rawg_iter, cron_multiplier=1)

    rename_rawg_upcm_task_cron = cron_24hr_clock(d_w='*', d_mo=1, mo='*', cron_mi=rawg_upcm_mi,
                                                 cron_hr=rawg_upcm_hr,
                                                 cron_iter=rawg_iter, cron_multiplier=1)

    celery_app.conf.beat_schedule = {
        'google_fetch_dev1': {'task': 'homepage.tasks.google_fetch_dev',
                              'schedule': g_dev_fetch_cron1,
                              'kwargs': ({'api_input': # placeholder}),
                              },

        'google_fetch_dev2': {'task': 'homepage.tasks.google_fetch_dev',
                              'schedule': g_dev_fetch_cron2,
                              'kwargs': ({'api_input': # placeholder}),
                              },

        'google_fetch_dev3': {'task': 'homepage.tasks.google_fetch_dev',
                              'schedule': g_dev_fetch_cron3,
                              'kwargs': ({'api_input': # placeholder}),
                              },

        'google_fetch_dev4': {'task': 'homepage.tasks.google_fetch_dev',
                              'schedule': g_dev_fetch_cron4,
                              'kwargs': ({'api_input': # placeholder}),
                              },

        'google_fetch_dev5': {'task': 'homepage.tasks.google_fetch_dev',
                              'schedule': g_dev_fetch_cron5,
                              'kwargs': ({'api_input': # placeholder}),
                              },

        'google_fetch_dev6': {'task': 'homepage.tasks.google_fetch_dev',
                              'schedule': g_dev_fetch_cron6,
                              'kwargs': ({'api_input': # placeholder}),
                              },

        'google_fetch_dev7': {'task': 'homepage.tasks.google_fetch_dev',
                              'schedule': g_dev_fetch_cron7,
                              'kwargs': ({'api_input': # placeholder}),
                              },

        'google_fetch_dev8': {'task': 'homepage.tasks.google_fetch_dev',
                              'schedule': g_dev_fetch_cron8,
                              'kwargs': ({'api_input': # placeholder}),
                              },

        'google_fetch_dev9': {'task': 'homepage.tasks.google_fetch_dev',
                              'schedule': g_dev_fetch_cron9,
                              'kwargs': ({'api_input': # placeholder}),
                              },

        'google_fetch_dev10': {'task': 'homepage.tasks.google_fetch_dev',
                               'schedule': g_dev_fetch_cron10,
                               'kwargs': ({'api_input': # placeholder}),
                               },

        'google_fetch_query1': {'task': 'homepage.tasks.google_fetch_query',
                                'schedule': g_query_fetch_cron1,
                                'kwargs': ({'api_input': # placeholder}),
                                },

        'google_fetch_query2': {'task': 'homepage.tasks.google_fetch_query',
                                'schedule': g_query_fetch_cron2,
                                'kwargs': ({'api_input': # placeholder}),
                                },

        'google_fetch_query3': {'task': 'homepage.tasks.google_fetch_query',
                                'schedule': g_query_fetch_cron3,
                                'kwargs': ({'api_input': # placeholder}),
                                },

        'google_fetch_query4': {'task': 'homepage.tasks.google_fetch_query',
                                'schedule': g_query_fetch_cron4,
                                'kwargs': ({'api_input': # placeholder}),
                                },

        'google_fetch_query5': {'task': 'homepage.tasks.google_fetch_query',
                                'schedule': g_query_fetch_cron5,
                                'kwargs': ({'api_input': # placeholder}),
                                },

        'google_fetch_query6': {'task': 'homepage.tasks.google_fetch_query',
                                'schedule': g_query_fetch_cron6,
                                'kwargs': ({'api_input': # placeholder}),
                                },

        'google_fetch_query7': {'task': 'homepage.tasks.google_fetch_query',
                                'schedule': g_query_fetch_cron7,
                                'kwargs': ({'api_input': # placeholder}),
                                },

        'google_fetch_query8': {'task': 'homepage.tasks.google_fetch_query',
                                'schedule': g_query_fetch_cron8,
                                'kwargs': ({'api_input': # placeholder}),
                                },

        'google_fetch_query9': {'task': 'homepage.tasks.google_fetch_query',
                                'schedule': g_query_fetch_cron9,
                                'kwargs': ({'api_input': # placeholder}),
                                },

        'google_fetch_query10': {'task': 'homepage.tasks.google_fetch_query',
                                 'schedule': g_query_fetch_cron10,
                                 'kwargs': ({'api_input': # placeholder}),
                                 },

        'rawg_dev_fetch': {'task': 'homepage.tasks.rawg_fetch',
                           'schedule': rawg_fetch_dev_cron,
                           'kwargs': ({'key': rawg_key,
                                       'rawg_dev': True}),
                           },

        'rawg_pop_fetch': {'task': 'homepage.tasks.rawg_fetch',
                           'schedule': rawg_fetch_pop_cron,
                           'kwargs': ({'key': rawg_key,
                                       'rawg_pop': True}),
                           },

        'rawg_upcm_fetch': {'task': 'homepage.tasks.rawg_fetch',
                            'schedule': rawg_fetch_upcm_cron,
                            'kwargs': ({'key': rawg_key,
                                        'rawg_upcm': True}),
                            },

        'rename_rawg_dev_task': {'task': 'homepage.tasks.rename_rawg_task',
                                 'schedule': rename_rawg_dev_task_cron,
                                 'kwargs': ({'rawg_dev': True}),
                                 },

        'rename_rawg_pop_task': {'task': 'homepage.tasks.rename_rawg_task',
                                 'schedule': rename_rawg_pop_task_cron,
                                 'kwargs': ({'rawg_pop': True}),
                                 },

        'rename_rawg_upcm_task': {'task': 'homepage.tasks.rename_rawg_task',
                                  'schedule': rename_rawg_upcm_task_cron,
                                  'kwargs': ({'rawg_upcm': True}),
                                  },

    }


cron_schedule()
