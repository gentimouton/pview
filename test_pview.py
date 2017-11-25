import unittest, os

import pygame

import pview 


class PviewTest(unittest.TestCase):
    def setUp(self):
        drivers = ['windib', 'directx', 'x11', 'dga', 'fbcon', 'directfb', 
                   'ggi', 'vgl', 'svgalib', 'aalib', 'dummy']
        for driver in drivers:
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print('Driver: {0} failed.'.format(driver))
                continue
            print('Driver: {0} loaded.'.format(driver))
            break
#         pygame.display.init()
        # baseline resolution is 640x480 and actual resolution is 1280x960
        pview.set_mode(size0=(640, 480), height=960)
    

    def test_pview(self):
        self.assertEqual(pview.size0, (640, 480))
        self.assertEqual(pview.screen, pygame.display.get_surface())
        self.assertEqual(pview.size, (1280, 960))
        
        
    def test_T(self):
        # translation from abstract resolution to actual resolution
        self.assertEqual(pview.T(10), 20)
        self.assertEqual(pview.T(4.4), 9)  # Always maps to ints
        self.assertEqual(pview.T(0.001), 1)  # Rounds away from 0
        self.assertEqual(pview.T([1, 2, 3]), [2, 4, 6])
        self.assertEqual(pview.T(1, 2, 3), [2, 4, 6])
        r1 = pygame.Rect(10, 10, 50, 50)
        r2 = pygame.Rect(20, 20, 100, 100)
        self.assertEqual(pview.T(r1), r2)
    
    
    def test_I(self):
        # identity
        self.assertEqual(pview.I(10), 10)
        self.assertEqual(pview.I(4.4), 5)  # Always maps to ints, ceiling
        self.assertEqual(pview.I(0.001), 1)  # Rounds away from 0
        self.assertEqual(pview.I([1, 2, 3]), [1, 2, 3])
        self.assertEqual(pview.I(1, 2, 3), [1, 2, 3])
        r1 = pygame.Rect(10, 10, 50, 50)
        self.assertEqual(pview.I(r1), r1)


    def test_fullscreen(self):
        if pygame.display.list_modes():  # platform can full screen
            def get_flags():
                return pygame.display.get_surface().get_flags()
            self.assertEqual(get_flags() & pygame.FULLSCREEN, 0)  # start windowed
            pview.toggle_fullscreen()
            self.assertEqual(get_flags() & ~pygame.FULLSCREEN, 0)  # full screen
            pview.toggle_fullscreen()
            self.assertEqual(get_flags() & pygame.FULLSCREEN, 0)  # is windowed 
            
            
    def test_change_mode(self):
        base_h = pview.h
        pview.set_mode(height=200)
        self.assertEqual(pview.h, 200)
        pview.set_mode(height=base_h)
        self.assertEqual(pview.h, base_h)
        
        
if __name__ == '__main__':
    unittest.main()
