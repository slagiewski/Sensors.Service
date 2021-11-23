import statistics


class DecreasingReadingSmoother:
    def __init__(self, repo, smoothing_radius):
        self.repository = repo
        self.smoothing_radius = smoothing_radius

    def smooth(self, current_reading : float) -> float :
        smoothing_radius = 25

        latest_readings = self.repository.get_latest_readings(take=10)

        if not len(latest_readings):
            self.repository.save_new_reading(current_reading)
            return current_reading

        latest_readings_mean = statistics.fmean(self.repository.get_latest_readings(take=10))

        if self.__is_reading_above_radius__(current_reading, smoothing_radius, latest_readings_mean):
            self.repository.save_new_reading(current_reading)
            latest_readings[0] = current_reading
            return statistics.fmean(latest_readings)

        if self.__is_reading_below_radius__(current_reading, smoothing_radius, latest_readings_mean):
            return latest_readings_mean

        if current_reading <= latest_readings_mean:
            self.repository.save_new_reading(current_reading)
            latest_readings[0] = current_reading

        return statistics.fmean(latest_readings)
        

    def __is_reading_below_radius__(self, current_reading, smoothing_radius, latest_readings_mean):
        return current_reading - latest_readings_mean < smoothing_radius

    def __is_reading_above_radius__(self, current_reading, smoothing_radius, latest_readings_mean):
        return current_reading - latest_readings_mean > smoothing_radius
