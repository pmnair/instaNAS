import subprocess
import crypt

class User(object):
	def __init__(s):
		s.users = []

	def groups(s, name):
		l = []
		try:
			r=subprocess.check_output(["groups", name], stderr=subprocess.STDOUT, shell=False)
			l = r.strip('\n').split(':')[-1].lstrip(' ').split(' ')
		except subprocess.CalledProcessError as e:
			print(e)
		return l

	def list(s):
		s.users = []
		r=subprocess.check_output(["grep", "/bin/.*bash", "/etc/passwd"], stderr=subprocess.STDOUT, shell=False)
		l=r.strip('\n').split('\n')
		for u in l:
			user = {}
			i = u.split(':')
			user['Name'] = i[0]
			user['Groups'] = s.groups(i[0])
			user['Home'] = i[5]
			s.users.append(user)
		return s.users

	def exists(s, name):
		l = s.list()
		return len([x for x in l if x['Name'] == name]) > 0

	def update(s, name, passwd):
		cpasswd=crypt.crypt(passwd, "123")
		cmd = ["usermod", "-p", cpasswd]

		try:
			r=subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)
			r=subprocess.check_output(['smbpasswd', '-x', name], stderr=subprocess.STDOUT, shell=False)
			p=subprocess.Popen(['smbpasswd', '-s', '-a', name], stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
			p.communicate(input=passwd + '\n' + passwd + '\n')

		except subprocess.CalledProcessError as e:
			pprint(e)
			return False
		return True

	def add(s, name, passwd, groups=None, home=None):
		try:
			cmd = ["useradd"]
			if groups:
				cmd += ["-G", groups]

			if home:
				cmd += ["-m", "-d", home]

			cpasswd=crypt.crypt(passwd, "123")
			cmd += ["-p" , cpasswd]
			cmd += ["-s" , "/bin/bash"]
			cmd += [name]
			#pprint(cmd)
			r=subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)
			p=subprocess.Popen(['smbpasswd', '-s', '-a', name], stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
			p.communicate(input=passwd + '\n' + passwd + '\n')
		except subprocess.CalledProcessError as e:
			pprint(e)
			return False
		return True

	def delete(s, name):
		try:
			r=subprocess.check_output(["userdel", "-r", name], stderr=subprocess.STDOUT, shell=False)
		except subprocess.CalledProcessError as e:
			print(e)
			return False
		return True
