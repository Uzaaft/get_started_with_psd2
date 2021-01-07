# Get started with the DNB PSD2 api.

The purpose if this repository is to serve as a starting point from which one can explore, and test the DnB API. This repository is based upon the Sandbox API. 

##### Provided under MIT License by Njord Technologies.
*Note: this library may be subtly broken or buggy. The code is released under
the MIT License – please take the following message to heart:*
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Getting Started

First, you should sign up at the [DNB Developer portal](https://developer.dnb.no), and read the Documentation there. 
## Requirements:

There are two requirements to get this code up and running. One is is to authenticate yourself when asking for consent from the DNB API. In the Sandbox API it is required to go to the link provided when asking for consent. This is handled by the code provided in this repository by using [Selenium](https://www.selenium.dev) and the [Chromium Driver](https://chromedriver.chromium.org/downloads). 
The [Selenium Documentation](https://www.selenium.dev/documentation/en/) is a great place to start if you have further enquiries about web automation.
The second requirement is to create, and download a certificate from [here](https://developer.dnb.no/profile/psd2). 
## Installation:
1. Make sure that you have Python 3.7 or higher installed on your computer. 
2. Make sure that you have pip installed. 
3. Install the library by using the following command: `pip install git+https://github.com/Njord-Technologies/get_started_with_psd` 

The following SSN's(Sosial Security Number) and ID for Corporate users are accesible in the Sandbox API:
| SSN/TB-ident | No. of accounts | No. of credit card accounts | Available context |
|--------------|-----------------|-----------------------------|-------------------|
| 31125453913  | 4               | 4                           | Retail            |
| 31125451740  | 2               | 6                           | Retail            |
| 31125459199  | 1               | 2                           | Retail            |
| 31125458990  | 3               | 2                           | Retail            |
| 31125461037  | 2               | 4                           | Retail            |
| 31125461118  | 1               | 2                           | Retail            |
| 31125452887  | 2               | 4                           | Retail            |
| 31125450361  | 3               | 2                           | Retail            |
| 31125458052  | 2               | 2                           | Retail            |
| 31125470982  | 2               | 2                           | Retail            |
| TB76688      | 4               | -                           | Corporate         |