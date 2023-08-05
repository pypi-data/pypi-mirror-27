py-cricket library for Roanuz Cricket API
=========================================

py-cricket library for Python using Roanuz Cricket API's. Easy to
install and simple way to access all Roanuz Cricket API's. Its a Python
library for getting Live Cricket Score, Cricket Schedule and Statistics.

Changes List:
-------------

::

    1.0.3:
        1.Access key, secret key and app id can also be accessed through Environmental variables.
        2.Ball by ball API has been added to the API list.

    1.0.2:
        1.File Storage Handler approach has been added for the Authentication.
        2.Authentication process has to be generated for every session.

Getting started
---------------

1. Install py-cricket using ``pip install py-cricket``

2. Create a Cricket API App here `My APP
   Login <https://www.cricketapi.com/login/?next=/apps/>`__

3. Import pycricket and create Authentication using
   'RcaFileStorageHandler' or 'RcaStorageHandler' approach.For accessing
   each API we need to get the 'AccessToken'

   .. rubric:: Example
      :name: example

   .. code:: rust

       //Use your Cricket API Application details below.

       //RcaStorageHandler
       import pycricket
       handler = pycricket.RcaStorageHandler()
       start = pycricket.RcaApp(access_key="Your_AccessKey", \
                               secret_key="Your_SecretKey", \
                               app_id="Your_APP_ID", \
                               store_handler=handler \
                              )

       'OR'

       //RcaFileStorageHandler(from environmental variable)

       Environmental variable:
           RCA_ACCESS_KEY = access_key
           RCA_SECRET_KEY = secret_key
           RCA_APP_ID = app_id

       handler = pycricket.RcaFileStorageHandler()
       start = pycricket.RcaApp(store_handler=handler)

       // After Completing Authentication you can successfully access the API's.

       start.get_match("iplt20_2016_g30") //Return Match information in json format
       start.get_season("dev_season_2016") //Return Season information in json format
       For more free API's visit : https://www.cricketapi.com/docs/freeapi/

List of Roanuz Cricket API
----------------------------

-  `Match API <https://www.cricketapi.com/docs/match_api/>`__
   start.get\_match("match\_key")
-  `Ball by ball
   API <https://www.cricketapi.com/docs/ball_by_ball_api/>`__
   start.get\_ball\_by\_ball("match\_key", over\_key="over\_key")
-  `Recent Matches
   API <https://www.cricketapi.com/docs/recent_match_api/>`__
   start.get\_recent\_matches()
-  `Recent Season
   API <https://www.cricketapi.com/docs/recent_season_api/>`__
   start.get\_recent\_seasons()
-  `Schedule API <https://www.cricketapi.com/docs/schedule_api/>`__
   start.get\_schedule()
-  `Season API <https://www.cricketapi.com/docs/season_api/>`__
   start.get\_season("season\_key")
-  `Season Stats
   API <https://www.cricketapi.com/docs/season_stats_api/>`__
   start.get\_season\_stats("season\_key")
-  `Season Points
   API <https://www.cricketapi.com/docs/season_points_api/>`__
   start.get\_season\_points("season\_key")
-  `Season Player Stats
   API <https://www.cricketapi.com/docs/season_player_stats_api/>`__
   start.get\_season\_player\_stats("season\_key", "player\_key")
-  `Over Summary
   API <https://www.cricketapi.com/docs/over_summary_api/>`__
   start.get\_overs\_summary("match\_key")
-  `News Aggregation
   API <https://www.cricketapi.com/docs/news_aggregation_api/>`__
   start.get\_news\_aggregation()

## Roanuz Cricket API This Library uses the Roanuz Cricket API for
fetching cricket scores and stats. Learn more about Litzscore Cricket
API on https://www.cricketapi.com/

## Contact: Feel free to call us anytime, We have an amazing team to
support you. You can contact us at : support@cricketapi.com
