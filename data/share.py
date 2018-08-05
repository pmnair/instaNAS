from pprint import pprint
import subprocess

class Share(object):
	def __init__(s):
		try:
			r=subprocess.check_output(["net", "conf", "import", "/etc/samba/smb.conf"], stderr=subprocess.STDOUT, shell=False)
		except subprocess.CalledProcessError as e:
			print(e)

	def list_confshares(s):
		try:
			r=subprocess.check_output(["net", "conf", "listshares"], stderr=subprocess.STDOUT, shell=False)
			l = r.strip('\n').split('\n')
			return l
		except subprocess.CalledProcessError as e:
			print(e)
			return None

	def list_usershares(s):
		try:
			r=subprocess.check_output(["net", "usershare", "list"], stderr=subprocess.STDOUT, shell=False)
			l = r.strip('\n').split('\n')
			return l
		except subprocess.CalledProcessError as e:
			print(e)
			return None

	def list(s):
		#l = s.list_confshares()
		l = s.list_usershares()
		return l

	def info(s, name):
		try:
			r=subprocess.check_output(["net", "usershare", "info", name], stderr=subprocess.STDOUT, shell=False)
			r = r.split('\n')
			inf = {}
			inf['Name'] = name
			for i in r:
				t = i.split('=')
				if len(t) > 1:
					inf[t[0].title()] = t[1]
			return inf
		except subprocess.CalledProcessError as e:
			print(e)
			return None

	def add(s, name, path, user, comment=None, rd=True, wr=False, guest=False):
		if comment == None:
			comment = name
		p = "d"
		if wr:
			p = "f"
		elif rd:
			p = "r"

		acl = "{0}:{1}".format(user, p)
		if guest:
			g_ok = 'guest_ok=y'
		else:
			g_ok = 'guest_ok=n'
		try:
			r=subprocess.check_output(["net", "usershare", "add", name, path, comment, acl, g_ok], stderr=subprocess.STDOUT, shell=False)
			print(r)
		except subprocess.CalledProcessError as e:
			print(e)
			return False
		return True

	def del_usershare(s, name):
		try:
			r=subprocess.check_output(["net", "usershare", "delete", name], stderr=subprocess.STDOUT, shell=False)
			print(r)
		except subprocess.CalledProcessError as e:
			print(e)
			return False
		return True

	def del_confshare(s, name):
		try:
			r=subprocess.check_output(["net", "conf", "delshare", name], stderr=subprocess.STDOUT, shell=False)
			print(r)
		except subprocess.CalledProcessError as e:
			print(e)
			return False
		return True

	def delete(s, name):
		if name in s.list_confshares():
			s.del_confshare(name)
			return True

		elif name in s.list_usershares():
			s.del_usershare(name)
			return True
		return False

	def refresh(s):
		try:
			r=subprocess.check_output(["service", "smbd", "restart"], stderr=subprocess.STDOUT, shell=False)
			print(r)
		except subprocess.CalledProcessError as e:
			print(e)
			return False
		return True
