# PKO-MPD
## Capacitated Vehicle routing problem with time window 

### Full description (LV):

Loģistikas uzņēmumam nepieciešams apkalpot 15 klientu objektus dienā. Uzņēmumam ir pieejamas 3 māšīnas, kas var pārvadāt 80 kravas vienības. Katrs klients var pieprasīt 5-20 kravas vienības. Uzņēmumam ir darba laiks no 8:00-17:00, kad tas veic piegādes. 17:00 visām mašīnām ir jāatrodas uzņēmumā. Uzņēmums vēlās pēc iespējas ātrāk veikt piegādes un sadalīt slodzi uz to darbiniekiem.

### To generate test data

``` python3 gen-test-data.py ```
#### This will generate a random distance matrix to each customer + company depot, and the demand for each costumer. Customer amount may be specified.

