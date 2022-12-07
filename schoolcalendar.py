from collections import OrderedDict
from datetime import datetime
import pickle

class SchoolCalendar:
    deadlines = {}

    def open(self):
        with open('saved/cal.pkl', 'rb') as inp:
            self.deadlines = pickle.load(inp)
        print(self.deadlines)

    def add_vak(self, vak):
        self.deadlines[vak] = {}
        self.save()

    def set_deadline(self, vak, date, deadline_title):
        self.deadlines[vak][deadline_title] = datetime.strptime(date, "%d/%m/%Y %H:%M")
        self.save()

    def set_exam_date(self, vak, date):
        self.set_deadline(vak, date, "Examen")
        self.save()

    def get_deadlines(self, vak):
        return OrderedDict(sorted(self.deadlines[vak].items(), key = lambda x:x[1]))

    def get_examens(self):
        res = {}
        for vak, dl in self.deadlines.items():
            res[vak] = dl['Examen']
        return OrderedDict(sorted(res.items(), key = lambda x:x[1]))

    def delete_vak(self, vak):
        self.deadlines.pop(vak)
        self.save()

    def delete_dl(self, vak, dl_title):
        self.deadlines[vak].pop(dl_title)
        self.save()

    def get_all_dl(self):
        days = {}
        for vak in self.deadlines.keys():
            dl_vak = self.get_deadlines(vak)
            for title, day in dl_vak.items():
                days[day] = (vak, title)
        return days

    def save(self):
        print(self.deadlines)
        with open('saved/cal.pkl', 'wb') as outp:
            pickle.dump(self.deadlines, outp, pickle.HIGHEST_PROTOCOL)
