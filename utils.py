from datetime import datetime, timedelta

class Utils:
    @staticmethod
    def time_elapsed(date_a=None, date_b=None, format='hours'):
        result = None

        if date_a and date_b and format in ['hours', 'days', 'months', 'years', 'raw']:
            date_a = date_a if isinstance(date_a, datetime) else Utils.getDateTime(date_a)
            date_b = date_b if isinstance(date_b, datetime) else Utils.getDateTime(date_b)

            interval = date_a - date_b

            if format == 'hours':
                result = interval.days * 24 + interval.seconds // 3600
            elif format == 'days':
                result = interval.days
            elif format == 'months':
                result = interval.days // 30
            elif format == 'years':
                result = interval.days // 365
            elif format == 'raw':
                result = interval

            if interval.days < 0:
                if format != 'raw':
                    result = -abs(result)

        return result

    @staticmethod
    def getDateTime(date=None, timezone='America/Bogota'):
        return datetime.strptime(date, '%Y-%m-%d') if date else datetime.now()

    @staticmethod
    def to_object(array):
        if not isinstance(array, list):
            return array

        obj = {}
        for key, value in array.items():
            key = key.lower().strip() if key else None
            if key is not None:
                obj[key] = Utils.to_object(value)
        return obj

    @staticmethod
    def to_string_day(value):
        days = [None, 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return days[value]

    @staticmethod
    def to_string_month(value):
        months = [None, 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return months[int(value)]

    @staticmethod
    def is_weekly(date):
        return Utils.getDateTime(date).weekday() == 0

    @staticmethod
    def is_biweekly(date):
        _date = Utils.getDateTime(date)
        last_day_of_month = _date.replace(day=28) + timedelta(days=4)
        last_day_of_month = last_day_of_month - timedelta(days=last_day_of_month.day)
        return _date.day == 15 or _date == last_day_of_month

    @staticmethod
    def is_monthly(date):
        _date = Utils.getDateTime(date)
        last_day_of_month = _date.replace(day=28) + timedelta(days=4)
        last_day_of_month = last_day_of_month - timedelta(days=last_day_of_month.day)
        return _date == last_day_of_month

    @staticmethod
    def date_interval(date_a, date_b, date_interval='P1D'):
        frecuency = {
            'P1D': '1 day',
            'P1W': '7 days',
            'P15D': '15 days',
            'P1M': '1 month',
            'P2M': '2 months',
            'P3M': '3 months',
            'P4M': '4 months',
            'P6M': '6 months',
            'P13M': '13 months',
            'P1Y': '1 year'
        }
        result = []

        if date_interval in ['P1D', 'P1W', 'P15D', 'P1M']:
            date_interval_string = '1 day' if date_interval != '' and date_interval in frecuency else 'first day of this month'
            start = Utils.getDateTime(date_a).replace(day=1)
            end = Utils.getDateTime(date_b).replace(day=1) + timedelta(days=32)
            end = end.replace(day=1) - timedelta(days=1)

            interval = timedelta(days=1) if date_interval == 'P1D' else timedelta(days=7) if date_interval == 'P1W' else timedelta(days=15) if date_interval == 'P15D' else timedelta(days=30)
            periods = [start + i * interval for i in range((end - start).days // interval.days + 1)]

            for dt in periods:
                key = dt.strftime('%Y-%m-%d')
                result.append({
                    'date_interval_string': date_interval,
                    'inicio': key,
                    'fin': (dt + interval - timedelta(days=1)).strftime('%Y-%m-%d')
                })

        else:
            date_interval_string = frecuency[date_interval] if date_interval != '' and date_interval in frecuency else 'first day of this month'
            start = Utils.getDateTime(date_a).replace(day=1)
            end = Utils.getDateTime(date_b).replace(day=1) + timedelta(days=32)
            end = end.replace(day=1) - timedelta(days=1)

            interval = timedelta(days=30)
            periods = [start + i * interval for i in range((end - start).days // interval.days + 1)]

            for dt in periods:
                key = dt.strftime('%Y-%m-%d')
                inicio = (dt - timedelta(days=365) if date_interval == 'P1Y' else dt - timedelta(days=int(date_interval[1:-1])*30)).strftime('%Y-%m-%d')
                result.append({
                    'date_interval_string': date_interval_string,
                    'inicio': inicio,
                    'fin': (dt + interval - timedelta(days=1)).strftime('%Y-%m-%d')
                })

        return Utils.to_object(result)

    @staticmethod
    def array_sort(array, field, order='ASC'):
        array.sort(key=lambda x: x[field], reverse=order == 'DESC')

if __name__ == "__main__":
    utils_instance = Utils()