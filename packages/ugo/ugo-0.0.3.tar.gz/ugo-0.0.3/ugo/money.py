class CNumber:
    c_dict = {}
    g_dict = {}
    x_dict = {}

    def __init__(self):
        self.c_dict = {1: u'', 2: u'拾', 3: u'佰', 4: u'仟'}
        self.x_dict = {1: u'元', 2: u'万', 3: u'亿', 4: u'兆'}
        self.g_dict = {0: u'零', 1: u'壹', 2: u'贰', 3: u'叁', 4: u'肆', 5: u'伍', 6: u'陆', 7: u'柒', 8: u'捌', 9: u'玖'}

    @staticmethod
    def __split__(c_data):
        g = len(c_data) % 4
        data_list = []
        lx = len(c_data) - 1
        if g > 0:
            data_list.append(c_data[0:g])
        k = g
        while k <= lx:
            data_list.append(c_data[k:k + 4])
            k += 4
        return data_list

    def __change__(self, cki):
        lk = len(cki)
        chk = u''
        for i in range(len(cki)):
            if int(cki[i]) == 0:
                if i < len(cki) - 1:
                    if int(cki[i + 1]) != 0:
                        chk = chk + self.g_dict[int(cki[i])]
            else:
                chk = chk + self.g_dict[int(cki[i])] + self.c_dict[lk]
            lk -= 1
        return chk

    def __zh__(self, data):
        if isinstance(data, str):
            if data.find('.') < 0:
                data = data + ".0"
        cdata = str(data).split('.')
        ckj = cdata[1]
        chk = u''
        cki = self.__split__(cdata[0])
        for i in range(len(cki)):
            if self.__change__(cki[i]) == '':
                chk = chk + self.__change__(cki[i])
            else:
                chk = chk + self.__change__(cki[i]) + self.x_dict[len(cki) - i]
        if len(ckj) == 1:
            if int(ckj[0]) == 0:
                chk = chk + u'整'
            else:
                chk = chk + self.g_dict[int(ckj[0])] + u'角整'
        else:
            if int(ckj[0]) == 0 and int(ckj[1]) != 0:
                chk = chk + u'零' + self.g_dict[int(ckj[1])] + u'分'
            elif int(ckj[0]) == 0 and int(ckj[1]) == 0:
                chk = chk + u'整'
            elif int(ckj[0]) != 0 and int(ckj[1]) != 0:
                chk = chk + self.g_dict[int(ckj[0])] + u'角' + self.g_dict[int(ckj[1])] + u'分'
            else:
                chk = chk + self.g_dict[int(ckj[0])] + u'角整'
        return chk


if __name__ == '__main__':
    print(CNumber().__zh__('21600190101000'))