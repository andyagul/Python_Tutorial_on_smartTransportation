# ---------- 第 09 章 异常处理 · 案例 9-2：用 raise 与 assert 做数据校验 ----------
# 对应知识点：9.4 raise 主动抛出与 assert 断言、9.3 except ... as e、9.2 finally
# 功能说明：对车牌与车速做合法性校验，不合法时主动抛出异常，由统一入口捕获并给出提示

def check_plate(plate):
    """车牌校验：长度 7 位、第 2 位大写字母"""
    assert len(plate) == 7, "车牌长度必须为 7 位，当前 " + str(len(plate)) + " 位"
    if not plate[1].isupper():
        raise ValueError("车牌第 2 位必须为大写字母：" + plate)
    return True


def check_speed(speed):
    """车速校验：0~300"""
    assert isinstance(speed, (int, float)), "车速必须是数字"
    if speed < 0 or speed > 300:
        raise ValueError("车速超出合理范围 0~300：" + str(speed))
    return True


def verify(plate, speed):
    try:
        check_plate(plate)
        check_speed(speed)
    except AssertionError as e:
        print("[断言失败]", e)
        return False
    except ValueError as e:
        print("[数据非法]", e)
        return False
    else:
        print("[校验通过]", plate, speed, "km/h")
        return True
    finally:
        print("   —— 校验流程结束 ——")


verify("京A12345", 62)
verify("京A123", 62)
verify("京a12345", 62)
verify("京A12345", 320)
verify("京B67890", "快")
