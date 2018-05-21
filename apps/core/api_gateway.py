from datetime import timedelta, datetime
import requests


def mount_query(device_id):
        def get_start_week(now):
            start_week = now.replace(hour=0, minute=0, second=0)
            one_day = timedelta(days=1)
            while start_week.weekday() != 1:
                start_week = start_week - one_day
            return start_week

        now = datetime.now()
        final_date = now.strftime('%Y-%m-%dT%H:%M:%S')
        daily_start_date = now.replace(
            hour=0, minute=0, second=0
        ).strftime('%Y-%m-%dT%H:%M:%S')

        weekly_start_date = get_start_week(now).strftime('%Y-%m-%dT%H:%M:%S')

        query = f'''
            query {{
                device(
                    deviceId: "{device_id}")
                    {{
                        daily_prod: totalPackages(
                            startDate:"{daily_start_date}",
                            finalDate:"{final_date}")
                        daily_init_prod: packages(
                            startDate:"{daily_start_date}",
                            finalDate:"{final_date}") {{time}}
                        weekly_prod: totalPackages(
                            startDate:"{weekly_start_date}",
                            finalDate:"{final_date}")
                        weekly_type_a: totalPackages(
                            startDate:"{weekly_start_date}",
                            finalDate:"{final_date}", type: "a")
                        weekly_type_b: totalPackages(
                            startDate:"{weekly_start_date}",
                            finalDate:"{final_date}", type: "b")
                        weekly_type_c: totalPackages(
                            startDate:"{weekly_start_date}",
                            finalDate:"{final_date}", type: "c")
                        weekly_type_d: totalPackages(
                            startDate:"{weekly_start_date}",
                            finalDate:"{final_date}", type: "d")
                }}
            }}
        '''
        r = requests.get(
            f'http://127.0.0.1:5000/graphql?query={query}'
        )
        return r.json()['data']['device'][0]
