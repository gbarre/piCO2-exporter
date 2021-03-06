from prometheus_client.core import GaugeMetricFamily

class Collector(object):
    def __init__(self, scd30, logger):
        self.scd30 = scd30
        self.logger = logger
        self.firmware = self.scd30.get_firmware_version()

    def collect(self):
        probe_co2 = GaugeMetricFamily(
            'probe_co2',
            'Show CO2 ppm metric',
            labels=["firmware_version"],
        )
        probe_temp = GaugeMetricFamily(
            'probe_temp',
            'Show temp metric',
            labels=["firmware_version"],
        )
        probe_humidity = GaugeMetricFamily(
            'probe_humidity',
            'Show humidity metric',
            labels=["firmware_version"],
        )

        self.logger.debug('================ Collect data ==================')

        m = self.getMetrics()
        if m is not None:
            probe_co2.add_metric(labels=[f'{self.firmware}'], value=m[0])
            probe_temp.add_metric(labels=[f'{self.firmware}'], value=m[1])
            probe_humidity.add_metric(labels=[f'{self.firmware}'], value=m[2])
        else:
            self.logger.warn('Nothing to return...')

        yield probe_co2
        yield probe_temp
        yield probe_humidity

        return

    def getMetrics(self):
        m = None
        if self.scd30.get_data_ready():
            m = self.scd30.read_measurement()
            if m is not None:
                self.logger.info(
                    f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}°C, rh: {m[2]:.2f}%"
                )
        return m
