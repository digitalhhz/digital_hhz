var ical = require('ical')
	, months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
var moment = require('moment')

ical.fromURL('https://calendar.google.com/calendar/ical/9fbtqhp79a3oqvq6v0ur434j2s%40group.calendar.google.com/private-6be31897ac099f4dbe5c28245f966a6b/basic.ics', {}, function(err, data) {
	var roomEvents = [];
	for (var k in data)
	{
		//console.log(k)
		if (data.hasOwnProperty(k) && String(data[k].location).includes("125")){
			data[k].end = moment(data[k].end);
			roomEvents.push(data[k]);
		}
	}
	var today = d => ( moment().year() == d.year() && moment().dayOfYear() == d.dayOfYear());
	var latestEventToday = roomEvents.filter(d => today(d.end)).reduce(moment().max);
	console.log(latestEventToday);
	//console.log(roomEvents[0], today(moment(roomEvents[0].end)));
});
