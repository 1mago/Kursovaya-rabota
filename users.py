import pymysql.cursors
import requests
import time

token = '785128a7b737ef53a5b4eee468070cd60edd278765cfdedf84b6018fef92a7fab9c5a9c1ee77e68fa3508'
version = 5.103
extended = 1
fields = 'bdate, mobile_phone,home_phone,friends,music,about'

class People(object):
    def __init__(self, id, ids, offset):
        self.id = id
        self.ids = ids
        self.offset = offset

    def users(self):
        user = []
        grup = []
        wall = []
        friend = []

        def users2():
            time.sleep(0.5)
            response = requests.get('https://api.vk.com/method/users.get',
                                    params={
                                        'access_token': token,
                                        'v': version,
                                        'user_ids': self.id,
                                        'fields': fields

                                    })
            data = response.json()['response']
            user.extend(data)
            return user

        user = users2()

        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='kursach',
                                     db='newest_schema')

        for item in user:
            try:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `json` (`№`,`id` , `first_name`,`last_name`,`bdate`,`mobile_phone`,`home_phone`,`music`,`about`) VALUES (%s,%s ,%s ,%s ,%s ,%s ,%s,%s,%s )"
                    cursor.execute(sql, (
                        item.get('№', [self.offset]), item.get('id'), item.get('first_name'),
                        item.get('last_name'), item.get('bdate'),
                        item.get('mobile_phone'), item.get('home_phone'),
                        item.get('music'), item.get('about')))
                connection.commit()
            except Exception as e:
                print(e)
        connection.close()
        try:
            def grups():
                time.sleep(0.5)
                response2 = requests.get('https://api.vk.com/method/groups.get',
                                         params={
                                             'access_token': token,
                                             'v': version,
                                             'user_id': self.ids,
                                             'extended': extended,
                                         })
                data = response2.json()['response']['items']
                grup.extend(data)
                return grup

            grup = grups()

            connection = pymysql.connect(host='127.0.0.1',
                                         user='root',
                                         password='kursach',
                                         db='newest_schema',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            for item in grup:
                try:
                    with connection.cursor() as cursor:
                        print(self.id[2:])
                        sql = "INSERT INTO `grups` (`№`,`id_grup`,`name_grup`,`screen_name_grup`, `json_idjson`) VALUES (%s,%s,%s,%s,%s)"
                        cursor.execute(sql, (
                            item.get('№', [self.offset]), item.get('id'), item.get('name'),
                            item.get('screen_name'), self.id[2:]))
                    connection.commit()
                except Exception as e:
                    print(e)
            connection.close()
        except Exception as e:
            print(e)

        try:
            def friends():
                fields = 'bdate'
                time.sleep(0.5)
                response1 = requests.get('https://api.vk.com/method/friends.get',
                                         params={
                                             'access_token': token,
                                             'v': version,
                                             'user_id': self.ids,
                                             'fields': fields

                                         })
                data = response1.json()['response']['items']
                friend.extend(data)
                return friend

            friend = friends()

            connection = pymysql.connect(host='127.0.0.1',
                                         user='root',
                                         password='kursach',
                                         db='newest_schema',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)

            for item in friend:
                try:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO `friends` (`№`,`id`,`first_name`,`last_name`, `json_idjson`) VALUES (%s,%s,%s,%s, %s)"
                        cursor.execute(sql, (
                            item.get('№', [self.offset]), item.get('id'), item.get('first_name'),
                            item.get('last_name'), self.id[2:]))
                    connection.commit()
                except Exception as e:
                    print(e)
            connection.close()
        except Exception as e:
            print(e)

        try:
            def walls():
                time.sleep(0.5)
                response1 = requests.get('https://api.vk.com/method/wall.get',
                                         params={
                                             'access_token': token,
                                             'v': version,
                                             'domain': self.id,
                                         })
                data = response1.json()['response']['items']
                wall.extend(data)
                return wall

            wall = walls()

            connection = pymysql.connect(host='127.0.0.1',
                                         user='root',
                                         password='kursach',
                                         db='newest_schema',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)

            for item in wall:
                try:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO `wall` (`№`,`id`,`likes`,`comments`,`reposts`, `json_idjson`) VALUES (%s,%s,%s,%s,%s,%s )"
                        cursor.execute(sql, (
                            item.get('№', [self.offset]), item.get('id'),
                            item.get('likes').get('count'),
                            item.get('comments').get('count'),
                            item.get('reposts').get('count'), self.id[2:]))
                    connection.commit()
                except Exception as e:
                    print(e)
            connection.close()
            for item in wall:
                likes(item)
        except Exception as e:
            print(e)


class likes():

    def __init__(self, item):
        self.owner_id = item.get('owner_id')
        self.id_wall = item.get('id')

        def likes():
            try:
                time.sleep(0.5)
                type = 'post'
                response1 = requests.get('https://api.vk.com/method/likes.getList',
                                         params={
                                             'access_token': token,
                                             'v': version,
                                             'owner_id': self.owner_id,
                                             'type': type,
                                             'item_id': self.id_wall
                                         })
                data = response1.json()['response']['items']
                return data
            except Exception as e:
                print(e)
        dict = {}
        id_friends = []
        try:
                id_friends.append({
                "id_friends": likes()})
                dict["id_friends"] = id_friends
        except Exception as e:
            print(e)
        connection = pymysql.connect(host='127.0.0.1',
                                     user='root',
                                     password='kursach',
                                     db='newest_schema',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            for item in id_friends:
                i = 0
                while i < len(item.get('id_friends')):
                    with connection.cursor() as cursor:
                        print(item.get('id_friends')[i])
                        sql = "INSERT INTO `likes` (`id_wall`,`id_friends`) VALUES (%s ,%s)"
                        cursor.execute(sql, (
                        item.get('id_wall', [self.id_wall]),
                        item.get('id_friends')[i]))
                        i += 1
                        connection.commit()

        except Exception as e:
            print(e)


if __name__ == "__main__":
    People1 = People('id155384397', '155384397', '1')
    People1.users()

    People2 = People('id122123897', '122123897', '2')
    People2.users()

    People3 = People('id226165635', '226165635', '3')
    People3.users()

    People4 = People('id204756182', '204756182', '4')
    People4.users()

    People5 = People('id169916098', '169916098', '5')
    People5.users()

    People6 = People('id287961694', '287961694', '6')
    People6.users()

    People7 = People('id226159703', '226159703', '7')
    People7.users()

    People8 = People('id207484334', '207484334', '8')
    People8.users()

    People9 = People('id160504052', '160504052', '9')
    People9.users()

    People10 = People('id156930209', '156930209', '10')
    People10.users()

    People11 = People('id62022070', '62022070', '11')
    People11.users()

    People12 = People('id364803419', '364803419', '12')
    People12.users()

    People13 = People('id164519173', '164519173', '13')
    People13.users()

    People14 = People('id253456309', '253456309', '14')
    People14.users()

    People15 = People('id203884671', '203884671', '15')
    People15.users()

    People16 = People('id205840517', '205840517', '16')
    People16.users()

    People17 = People('id487119415', '487119415', '17')
    People17.users()

    People18 = People('id18864498', '18864498', '18')
    People18.users()

    People19 = People('id444545086', '18864498', '19')
    People19.users()

    People20 = People('id547652798', '547652798', '20')
    People20.users()

    People21 = People('id72511618', '72511618', '21')
    People21.users()

    People22 = People('id192260451', '192260451', '22')
    People22.users()

    People23 = People('id132033643', '132033643', '23')
    People23.users()
