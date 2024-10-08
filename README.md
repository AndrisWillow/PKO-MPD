# PKO-MPD
## Capacitated Vehicle routing problem with time window
#### Program is tested using Python 3.10.12

### Full description (LV):

Loģistikas uzņēmumam nepieciešams apkalpot 15 klientu objektus dienā. Uzņēmumam ir pieejamas 3 māšīnas, kas var pārvadāt 80 kravas vienības. Katrs klients var pieprasīt 5-20 kravas vienības. Uzņēmumam ir darba laiks no 8:00-17:00, kad tas veic piegādes. 17:00 visām mašīnām ir jāatrodas uzņēmumā. Uzņēmums vēlās pēc iespējas ātrāk veikt piegādes un sadalīt slodzi uz to darbiniekiem. Mašīnām braucot pa to pašu ceļu turp un atpakaļ ceļš var atšķirties.

### To generate test data

``` python3 gen-test-data.py ```
#### This will generate a random distance matrix (Asymmetric i.e. AB != BA) to each customer + company depot, and the demand for each costumer. Customer amount may be specified.
#### Company depot is the 0th element.

### To run algorithm

``` python3 PKO-MD.py ```