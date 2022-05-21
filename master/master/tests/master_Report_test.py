from master.app.Report import Timestamp, Timereport

import pytest, copy


list_values_right_1 = [
        ('01:12:46',0,0,'01:12:40'),
        ('00:00:00',1,1,'00:00:00'),
        ('23:59:59',1,1,'23:59:50'),
        ('01:12:46',4999,4999, '01:12:40'),
    ]

list_values_wrong_1 = [
        ('01:12:46',0,-1),
        ('01:12:46',-1,0),
        ('00:00:-10',1,1),
        ('23:59:60',1,1),
        ('23:69:59',1,1),
        ('23:59:60',5000,1),
        ('23:59:60',1,5000),
        ('24:12:46',4999,4999),
    ]
t1 = Timestamp( '22:12:40', 3,11)
t2 = Timestamp( '22:12:44', 2,1)
t3 = Timestamp( '22:12:50', 5,4)
t4 = Timestamp( '22:12:52', 6,3)
t5 = Timestamp( '22:12:54', 7,2)
t6 = Timestamp( '22:12:56', 8,1) 
@pytest.mark.testclass
def test_Timestamp_init_right():
    try:
        for value in list_values_right_1:
                t = Timestamp(value[0], value[1], value[2])
                excpected = value[3]
                assert excpected == t.timestamp
    except:
        assert False

@pytest.mark.testclass
def test_Timestamp__init_wrong_():
    try:
        for value in list_values_wrong_1:
                t = Timestamp(value[0], value[1], value[2])
                assert False
    except:
        assert True

@pytest.mark.testclass
def test_Timereport_init_right():
   try:    
        l_t = [t1,t2,t3]
        T1 = Timereport('Simulation_name',l_t)
   except:
        assert False
@pytest.mark.testclass
def test_Timestamp_eq():
    assert t1 == t2
    assert t1 != t3


@pytest.mark.testclass
def test_Timestamp_add_right():
    t4 = t1 + t2
    assert t1 != t3
    assert t4.ok == (t2.ok + t1.ok)
    assert t4.nok == (t2.nok + t1.nok)
    assert t4.timestamp == t1.timestamp

@pytest.mark.testclass
def test_Timestamp_add_wrong():
    try: 
        t1 + t3
        assert False
    except:
        assert True
@pytest.mark.testclass
def test_Timereport_add_timestamp():
    l_t = [t1]
    T1 = Timereport('Simulation_name', l_t)
    T1.add_timestamp(t2)
    T1.add_timestamp(t3)
    
    assert  T1.l_timestamps[0].ok == int(t2.ok + t1.ok)
    assert  T1.l_timestamps[0].nok == int(t2.nok + t1.nok)
    assert  T1.l_timestamps[0].timestamp == t1.timestamp
    assert  T1.l_timestamps[1] == t3

@pytest.mark.testclass
def test_Timereport_eq():
    T1 = Timereport('Simulation_name', [])
    T2 = Timereport('Simulation_name', [])
    T3 = Timereport('Simulation-name', [])
    assert T1 == T2
    assert T1 != T3

@pytest.mark.testclass
def test_Timereport_add_right():
    T1 = Timereport("Simulation_name",[t1])
    T1.add_timestamp(t3)
    T2 = Timereport("Simulation_name",[t2])
    T2.add_timestamp(t6)
    assert T2 == T1
    
    M1 = copy.copy(T1)
    M2 = copy.copy(T2)
    print("before:")
    print("T1:",str( T1 ) ,"\nT2",str(T2) )
    tt1 = T2 + T1
    tt2 = T1 + T2
    tr = t1 + t2    
    assert tt1.l_timestamps[0] == t1 + t2
    assert tt2.l_timestamps[0] == t1 + t2


    assert tt1.l_timestamps[1] == t6 + t3
    assert tt2.l_timestamps[1] == t6 + t3
    print("after:")
    print("T1:",str(T1),"\nT2",str(T2) )
    assert M1.l_timestamps[1] == T1.l_timestamps[1]
    assert M2.l_timestamps[1] == T2.l_timestamps[1]
@pytest.mark.testclass
def test_Timereport_add_wrong():
    T1 = Timereport("Simulation_name",[t1])
    T2 = Timereport("Simulation_name",[])
    T3 = Timereport("Simulation_name",[])
    def _try(r1,r2):
        try: 
            r1 + r2
            assert False
        except:
            assert True
    _try(T1,T2)
    _try(T3,T1)
    _try(T2,T3)
@pytest.mark.testclass
def test_Timestamp_simple():
    assert isinstance(t1.simple(),tuple)
    assert t1.simple()[0] == t1.timestamp
    assert t1.simple()[1] == t1.ok
    assert t1.simple()[2] == t1.nok

@pytest.mark.testclass
def test_Timereport_simple():
    T1 = Timereport("Simulation_name",[t1])
    t = T1.simple()
    assert t['name'] == "Simulation_name"
    assert t['timestamps'][0][0] == t1.timestamp
    assert t['timestamps'][0][1] == t1.ok
    assert t['timestamps'][0][2] == t1.nok


@pytest.mark.testclass
def test_Timereport_put():
    T1 = Timereport("Simulation_name",[t1,t3])
    t = T1.simple()
    T  = Timereport()
    T.put(t)
    assert T == T1
    assert len(T.l_timestamps) == len(T1.l_timestamps)
    for i in range(len(T.l_timestamps)):
        assert T1.l_timestamps[i] == T.l_timestamps[i]

