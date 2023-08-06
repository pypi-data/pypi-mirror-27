Change log
----------

- **0.0.6** 2017/12/xx

    - Beginning with the webserver.
      A first page with last datas is available (in french sorry).
    - Data base update. Add long description to server.
      Please run V004to005.sql available on http://static.frkb.fr/wdwapp
    - Removed tests.

- **0.0.4** 2017/12/25

	- Remove return value.
    - Change logging system to manage different levels (debug, error, warning,
      etc.). In this way, for example, warnings can be send by mail from cron.
      This implies mail option from log() have been removed.
    - Suppress of backup file. Replaced by sensor_data table.
      This table is indexed with sensor ID and timestamp so it is easier to
      re-process data for a new sensor (re-process part need to be written).

- **0.0.3** 2017/12/22

	- Rounding results to avoid truncate warning during database update.
    - Avoid to insert already existing weather data.

- **0.0.1** 2017/12/21

	First version.
