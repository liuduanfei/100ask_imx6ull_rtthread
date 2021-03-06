import os

# toolchains options
ARCH='arm'
CPU='cortex-a'
CROSS_TOOL='gcc'

if os.getenv('RTT_CC'):
    CROSS_TOOL = os.getenv('RTT_CC')

# only support GNU GCC compiler.
PLATFORM  = 'gcc'
EXEC_PATH = '/usr/bin'

if os.getenv('RTT_EXEC_PATH'):
    EXEC_PATH = os.getenv('RTT_EXEC_PATH')

BUILD = 'debug'

if PLATFORM == 'gcc':
    # toolchains
    PREFIX = 'arm-none-eabi-'
    CC = PREFIX + 'gcc'
    CXX = PREFIX + 'g++'
    AS = PREFIX + 'gcc'
    AR = PREFIX + 'ar'
    LINK = PREFIX + 'gcc'
    TARGET_EXT = 'elf'
    SIZE = PREFIX + 'size'
    OBJDUMP = PREFIX + 'objdump'
    OBJCPY = PREFIX + 'objcopy'

    DEVICE = ' -march=armv7-a -mtune=cortex-a7 -ftree-vectorize -ffast-math -mfloat-abi=softfp'
    CFLAGS = DEVICE + ' -Wall -mfpu=vfpv3-d16'
    AFLAGS = ' -c' + DEVICE + ' -x assembler-with-cpp -D__ASSEMBLY__'
    LINK_SCRIPT = 'imx6ull.lds'
    LFLAGS = DEVICE + ' -Wl,--gc-sections,-Map=rtthread.map,-cref,-u,system_vectors'+\
                      ' -T %s' % LINK_SCRIPT

    CPATH = ''
    LPATH = ''

    # generate debug info in all cases
    AFLAGS += ' -gdwarf-2'
    CFLAGS += ' -g -gdwarf-2'

    if BUILD == 'debug':
        CFLAGS += ' -O0'
    else:
        CFLAGS += ' -O2'

    POST_ACTION = OBJCPY + ' -O binary $TARGET rtthread.bin\n' +\
                  SIZE + ' $TARGET \n' +\
				  'python mkimage.py -d imx6ul-dcdConfig.csv -a 0x80001000 -b rtthread.bin -i rtthread.imx -g rtthread.img\n'
