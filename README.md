# PKO-MPD
## Capacitated Vehicle routing problem with time window
#### Program is tested using Python 3.10.12

### Full description (LV):

Loģistikas uzņēmumam nepieciešams apkalpot 15 klientu objektus dienā. Uzņēmumam ir pieejamas 3 māšīnas, kas var pārvadāt 80 kravas vienības. Katrs klients var pieprasīt 5-20 kravas vienības. Uzņēmumam ir darba laiks no 8:00-17:00, kad tas veic piegādes. 17:00 visām mašīnām ir jāatrodas uzņēmumā. Uzņēmums vēlās pēc iespējas ātrāk veikt piegādes un sadalīt slodzi uz to darbiniekiem. Mašīnām braucot pa to pašu ceļu turp un atpakaļ ceļš var atšķirties.

### To generate test data

``` python3 gen-test-data.py {input_json} {num_clients}```
#### This will generate a random distance matrix (Asymmetric i.e. AB != BA) to each customer + company depot, and the demand for each costumer. Customer amount may be specified.
#### Company depot is the 0th element.

### To run algorithm

``` python3 PKO-MD.py {input_json} {num_truks} {num_generations} {population}```
#### There are also defualt paramaters set


### Test cases:

#### 1:
``` python3 gen-test-data.py test-data.json 15 ```
``` python3 PKO-MD.py test-data.json 3 50 4 ```

#### 2:
``` python3 gen-test-data.py test-data2.json 45 ```
``` python3 PKO-MD.py test-data2.json 3 50 4 ```

#### 3:
``` python3 gen-test-data.py test-data3.json 1000 ```
``` python3 PKO-MD.py test-data3.json 90 200 10 ```

#### 4:
``` python3 gen-test-data.py test-data4.json 2000 ```
``` python3 PKO-MD.py test-data4.json 190 200 10 ```