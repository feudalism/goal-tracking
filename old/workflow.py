from openpyxl import load_workbook
import sys

import categories
import db
import worksheet

from paths import AG_FILEPATH, NG_FILEPATH



# Add new goals
worksheet.add_new_goals(newpath=NG_FILEPATH, oldpath=AG_FILEPATH)
olddata, ws, wb = worksheet.extract_data(AG_FILEPATH)
newdata, _, _ = worksheet.extract_data(NG_FILEPATH)

# Init database
database = db.init_db()
db.data_entry(newdata, database)

# Check if goals are removed
worksheet.remove_goal_from_db(database, oldpath=AG_FILEPATH)

# Update categories
cats = categories.get(olddata)
categories.save_to_file(cats)

# Steps
worksheet.create_sheets(wb, cats)
for cat in cats:
	worksheet.update_cat_goals(wb, cat, database)
	wb.save(AG_FILEPATH)

# Close
db.close(database)
	
