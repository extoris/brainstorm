import sqlite3

conn = sqlite3.connect("audio.db")
cursor = conn.cursor()
conn.commit()
cursor.execute("""CREATE TABLE voices
                  (word text, translate text, voices_id text)
               """)

voices = [('proposes','предлагает','CQACAgIAAxkDAAIM4mJQHg9arGNUdtN-jQwweTDwvnWUAAIYFAACUCSASt93YeceEj8YIwQ'),
          ('transcribed','транскрибируемый','CQACAgIAAxkDAAIM42JQHhJSlaNJGE-OeDFjKfdROxVgAAIZFAACUCSASip1015sdngtIwQ'),
          ('erickson','Эриксон','CQACAgIAAxkDAAIM5GJQHhYCuXjW1oRTU2e5k3d4OHaEAAIaFAACUCSASmiE-y88Pu_rIwQ'),
          ('speciality','специальность','CQACAgIAAxkDAAIM5WJQHhnQGakvAafhI83iveSGUrkSAAIbFAACUCSASiL7xRFbHSiOIwQ'),
          ('introduces','вводит','CQACAgIAAxkDAAIM5mJQHhxuRvKHG6qLa-4YXi9tuu4OAAIcFAACUCSASrVsSIsH4tPOIwQ'),
          ('intrinsic','присущий','CQACAgIAAxkDAAIM52JQHh8Bx0Akb17Uav3eMibYjg4iAAIdFAACUCSASktlJuxoGso7IwQ'),
          ('settled','установившийся','CQACAgIAAxkDAAIM6GJQHiNeHe3f4pX5TBFNQ3UWoW3dAAIeFAACUCSASka8WZx1jOL1IwQ'),
          ('corrupt','развращать','CQACAgIAAxkDAAIM6WJQHiahxVasrUT-qo-lg-xMyqqPAAIfFAACUCSASkD7lkwm6gxdIwQ'),
          ('linkages','установление связей','CQACAgIAAxkDAAIM6mJQHinE2H7NjgwagxsjzERz7B6xAAIgFAACUCSASuUAATmAHNPTxSME'),
          ('creators','творческие работники','CQACAgIAAxkDAAIM62JQHizxYmd4YNgvJHy3GWl1Vd9hAAIhFAACUCSASvMpczm1nmFkIwQ'),]

cursor.executemany("INSERT INTO voices VALUES (?,?,?)", voices)
conn.commit()
