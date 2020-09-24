#!/usr/bin/python3

import unittest
import subprocess
from subprocess import CalledProcessError

class test_tpm2(unittest.TestCase):
    def test_get_random(self):
        subprocess.run(['tssgetrandom', '-by', '10'], check=True, capture_output=True)

class test_accelerometer(unittest.TestCase):
    '''
    Test expects system standing bottom-down
    '''
    def get_accel(self, axis):
        '''
        Read accelelration in m/s^2
        '''
        raw = subprocess.run(['iio_attr', '-q', '-c', 'lsm6dsm_accel', axis, 'raw'],
                             check=True, capture_output=True, text=True)
        scale = subprocess.run(['iio_attr', '-q', '-c', 'lsm6dsm_accel', axis, 'scale'],
                             check=True, capture_output=True, text=True)
        return float(raw.stdout.strip()) * float(scale.stdout.strip())
        
    def test_accel_x(self):
        value = self.get_accel('accel_x')
        self.assertTrue(-1 <= value <= 1)

    def test_accel_y(self):
        value = self.get_accel('accel_y')
        self.assertTrue(-1 <= value <= 1)
        
    def test_accel_z(self):
        value = self.get_accel('accel_z')
        self.assertTrue(9 <= value <= 11)
        
class test_gyro(unittest.TestCase):
    '''
    Test expects system not rotating
    '''
    def get_level(self, axis):
        '''
        Read angular velocity in dps
        '''
        raw = subprocess.run(['iio_attr', '-q', '-c', 'lsm6dsm_gyro', axis, 'raw'],
                             check=True, capture_output=True, text=True)
        scale = subprocess.run(['iio_attr', '-q', '-c', 'lsm6dsm_gyro', axis, 'scale'],
                             check=True, capture_output=True, text=True)
        return float(raw.stdout.strip()) * float(scale.stdout.strip())
        
    def test_accel_x(self):
        value = self.get_level('anglvel_x')
        self.assertTrue(-3 <= value <= 3)

    def test_accel_y(self):
        value = self.get_level('anglvel_y')
        self.assertTrue(-3 <= value <= 3)
        
    def test_accel_z(self):
        value = self.get_level('anglvel_z')
        self.assertTrue(-3 <= value <= 3)
        
class test_gpu(unittest.TestCase):
    def test_benchmark(self):
        p = subprocess.run(['glmark2-es2-wayland', '-b', 'build:duration=1.0'], check=True, capture_output=True, text=True)
        renderer = 'Vivante GC2000 rev 5108'
        self.assertTrue(renderer in p.stdout, f'Renderer "{renderer}" not detected in output:\n{p.stdout}')
        
class test_status_led(unittest.TestCase):
    '''
    Verify interface doesn't return error, no visual verification
    '''
    def run_test(self, led):
        subprocess.run(['status-led', led], check=True, capture_output=True)
        subprocess.run(['status-led', led, 'blink'], check=True, capture_output=True)
        subprocess.run(['status-led', 'off'], check=True, capture_output=True)
        
    def test_red(self):
        self.run_test('red')
        
    def test_green(self):
        self.run_test('green')
        
    def test_yellow(self):
        self.run_test('yellow')
        
class test_rs232_1(unittest.TestCase):
    '''
    Loopback test:
    tx -> rx
    rts -> cts
    '''
    def setUp(self):
        self.dev = '/dev/ttymxc1'
        
    def loopback(self, baudrate, rtscts=False):
        cmd = ['uart_loopback', '-b', str(baudrate), '-t', '1', self.dev]
        if rtscts:
            cmd.append('--rtscts')
        subprocess.run(cmd, check=True, capture_output=True)
        
    def test_9600(self):
        self.loopback(9600)
        
    def test_115200(self):
        self.loopback(115200)
        
    def test_9600_rtscts(self):
        self.loopback(9600, rtscts=True)
        
    def test_115200_rtscts(self):
        self.loopback(115200, rtscts=True)
        
class test_rs232_2(test_rs232_1):
    def setUp(self):
        self.dev = '/dev/ttymxc3'

class test_rs485_1_2(unittest.TestCase):
    '''
    Loopback test:
    RS485_A -> RS485_B
    '''
    @classmethod
    def setUpClass(cls):
        cls.dev1 = '/dev/ttyVEC0'
        cls.res1 = '/sys/class/gpio/gpio489/value'
        cls.j17081 = '/sys/class/gpio/gpio488/value'
        cls.dev2 = '/dev/ttyVEC1'
        cls.res2 = '/sys/class/gpio/gpio485/value'
        cls.j17082 = '/sys/class/gpio/gpio484/value'
        
    def setUp(self):
        self.set_gpio(self.res1, 0)
        self.set_gpio(self.res2, 0)
        self.set_gpio(self.j17081, 0)
        self.set_gpio(self.j17082, 0)
        
    def tearDown(self):
        self.set_gpio(self.res1, 0)
        self.set_gpio(self.res2, 0)
        self.set_gpio(self.j17081, 0)
        self.set_gpio(self.j17082, 0)
        
    def loopback(self, baudrate):
        cmd = ['uart_loopback', '-b', str(baudrate), '-t', '1', '--rs485', self.dev1, self.dev2]
        subprocess.run(cmd, check=True, capture_output=True)
        
    def set_gpio(self, gpio, value):
        with open(gpio, 'w') as f:
            f.write(str(int(value)))
            
    def test_115200_termination_1(self):
        self.set_gpio(self.res1, 1)
        self.loopback(115200)
    
    def test_115200_termination_2(self):
        self.set_gpio(self.res2, 1)
        self.loopback(115200)
        
    def test_9600_termination_1(self):
        self.set_gpio(self.res1, 1)
        self.loopback(9600)
    
    def test_9600_termination_2(self):
        self.set_gpio(self.res2, 1)
        self.loopback(9600)
    
    def test_j1708(self):
        self.set_gpio(self.j17081, 1)
        self.set_gpio(self.j17082, 1)
        self.loopback(9600)
        
class test_can_1_2(unittest.TestCase):
    '''
    Loopback test:
    CAN_1 -> CAN_2
    '''
    @classmethod
    def setUpClass(cls):
        cls.dev1 = 'can0'
        cls.res1 = '/sys/class/gpio/gpio95/value'
        cls.en1 = '/sys/class/gpio/gpio508/value'
        cls.sb1 = '/sys/class/gpio/gpio27/value'
        cls.dev2 = 'can1'
        cls.res2 = '/sys/class/gpio/gpio9/value'
        cls.en2 = '/sys/class/gpio/gpio509/value'
        cls.sb2 = '/sys/class/gpio/gpio106/value'
        
    def setUp(self):
        self.set_gpio(self.res1, 0)
        self.set_gpio(self.res2, 0)
        # enable transceiver 1
        self.set_gpio(self.en1, 1)
        self.set_gpio(self.sb1, 0)
        # enable transceiver 2
        self.set_gpio(self.en2, 1)
        self.set_gpio(self.sb2, 0)
        
    def tearDown(self):
        self.set_gpio(self.res1, 0)
        self.set_gpio(self.res2, 0)
        self.set_gpio(self.en1, 0)
        self.set_gpio(self.sb1, 0)
        self.set_gpio(self.en2, 0)
        self.set_gpio(self.sb2, 0)
    
    def config_device(self, dev, bitrate):
        subprocess.run(['ifconfig', dev, 'down'], check=True, capture_output=True)
        subprocess.run(['canconfig', dev, 'bitrate', str(bitrate)], check=True, capture_output=True)
        subprocess.run(['canconfig', dev, 'restart-ms', '1000'], check=True, capture_output=True)
        subprocess.run(['ifconfig', dev, 'up'], check=True, capture_output=True)
        
    def loopback(self, bitrate):
        self.config_device(self.dev1, bitrate)
        self.config_device(self.dev2, bitrate)
        cmd = ['can_loopback', self.dev1, self.dev2, str(bitrate), '1']
        subprocess.run(cmd, check=True, capture_output=True)
        
    def set_gpio(self, gpio, value):
        with open(gpio, 'w') as f:
            f.write(str(int(value)))
  
    def test_1000000_no_termination(self):
        with self.assertRaises(CalledProcessError):
            self.loopback(1000000)
                 
    def test_125000_termination_1(self):
        self.set_gpio(self.res1, 1)
        self.loopback(125000)
        
    def test_125000_termination_2(self):
        self.set_gpio(self.res2, 1)
        self.loopback(125000)
        
    def test_1000000_termination_1(self):
        self.set_gpio(self.res1, 1)
        self.loopback(1000000)
        
    def test_1000000_termination_2(self):
        self.set_gpio(self.res2, 1)
        self.loopback(1000000)

if __name__ == '__main__':
    unittest.main()
