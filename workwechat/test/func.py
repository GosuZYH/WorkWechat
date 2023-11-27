from datetime import datetime, timedelta
import configparser

def for_loop():
	# dict1 = {}
	# i = 0
	# while True:
	# 	i += 1
	# 	if i > 3:
	# 		dict1[i] = True
	# 		dict1[i] = True
	# 		dict1[i] = True
	# 	else:
	# 		dict1[i] = False
	# 	if i > 6:
	# 		break

	# try:
	# 	if dict1[10]:
	# 		pass
	# except:
	# 	dict1[10] = True

	# print(dict1)

	# time_flag = 30
	# timeset = '10:00'
	# flag_time = (datetime.now() - timedelta(days=time_flag)).strftime('%Y年%m月%d日') + timeset
	# flag_time = datetime.strptime(flag_time,'%Y年%m月%d日%H:%M')
	# print(flag_time)
	pass

def get_config_time():
	config = configparser.ConfigParser()
	config.read('config/config.ini', encoding='utf-8')
	try:
		sopgapday = config.get('stop sending time', 'sopdaygap')
		stoptime = config.get('stop sending time', 'soptime')
		print(sopgapday,stoptime)
	except:
		sopgapday = 1
		stoptime = '22:00'

	if not sopgapday.isdigit() or ':' not in stoptime:
		sopgapday = 1
		stoptime = '22:00'

	return sopgapday,stoptime

if __name__ == '__main__':
	a,b = get_config_time()
	print(a,b)


