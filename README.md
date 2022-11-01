# MS
Master's Thesis:  Design and implementation of an adaptive digital communication system using USRP devices. The Thesis is available in  https://digibuo.uniovi.es/dspace/handle/10651/60640

## About this repo
This is the GNU Radio out-of-tree module and the grc and Python files along with the Thesis memory. The basic ideas for this system (explain in detail in the Thesis) are:
* One Tx and one Rx with a feedback channel of much less bandwidth that the main channel.
* Tx sends data in packets. BPSK is always used on the Header, options for the Payload are (BPSK, QPSK, 16-QAM, and 64-QAM).
* The modulation used at the Payload is chosen based on the Rx feedback and an Error Probability threshold that the user inputs depending on the application.
* Apart from the feature of adaptive modulation, the most common effects in a mobile channel such as Doppler Effect, multipath or fast fading are considered. For example, packet detection; time/symbol synchronization; channel equalization (although just blind equalizers are used); or adaptive decision boundaries are implemented, apart from a CRC code for each packet.
The Thesis is written in Spanish, but the name of the blocks and the code comments are in English


## Pre-requisites
GNU Radio 3.9. Two USRP B210 were used for development and testing, although this work can be implemented with any full-duplex USRP model with no changes, and even with any other Software Defined Radio device GNU-Radio-compatible with few modifications.

For installation of the out-of-tree firs remove the build folder:

```console
$ cd gr-TFMv5
$ rm -r build
$ mkdir build
$ cd build
$ cmake ../
$ make
$ sudo ldconfig
```
For more info: https://wiki.gnuradio.org/index.php/OutOfTreeModules
