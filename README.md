# NewEmployeeApp
NewEmployeeApp is a Python-based application designed to simplify the onboarding process for new employees. 
It features a user-friendly graphical interface for entering employee details, and automatically generates a customized onboarding checklist in PDF format. 
The app uses SQLite for data management and FPDF for PDF generation.

## Installation

To use the NewEmployeeApp, follow these steps:

```bash
git clone https://github.com/CodePapayas/NewEmployeeApp.git
cd NewEmployeeApp
# Install the required packages
pip install tk fpdf sqlite3
```

## Usage
Run the application using Python:
```bash
python new_employee_app.py
```
Fill in the employee details and press "confirm" to generate an entry in a SQlite database (for retrieval upon employee exit) as well as a PDF onboarding checklist.
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
