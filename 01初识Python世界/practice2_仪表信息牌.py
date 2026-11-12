# 车载仪表自检信息输出
print("项目\t数值\t单位")          # 表头：三列名称
print("车速\t62\tkm/h")            # 实时车速
print("剩余电量\t78\t%")            # 动力电池 SOC
print("续航\t316\tkm")              # 剩余续航里程
print("挡位\tD\t-")                # 当前挡位

# 一条 print 内用 \n 输出两行收尾信息
print("自检完成\n系统正常，可以起步")
