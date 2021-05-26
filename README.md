# Fuzzy-DNA-Search-API

## Description:
As part of the CS-201 (Data Structures II) course at [Habib University](https://habib.edu.pk/), this is an implementation of Fuzzy DNA Search using ```FM Index``` as the primary data structure.
This is the backend API for the [Fuzzy DNA Search application](https://github.com/FaazAbidi/Fuzzy-DNA-Search).

## Deployment:
API is deployed at [Heroku](https://fm-index.herokuapp.com/).

## Endpoints:
- [/search](https://fm-index.herokuapp.com/search)
- [/preloaded](https://fm-index.herokuapp.com/preloaded)

### Search Endpoint:
The search endpoint takes a post request with the following entries:
  - DNA file in ```.txt``` format.
  - The substring to search for.

It creates the Index of the DNA file and then queries for the substring in the index. The result is a ```json``` object with scores as keys and a list of indices denoting where the substring is present in the DNA string. See Sample Output below.

### Preloaded Endpoint:
The preloaded endpoint has 2 real DNAs already indexed for users to play with. The endpoint takes the following entries:
  - marker denoting which index file to search in. Marker should be either ```1``` or ```2```.
  - The substring to search for.

It loads the desired index and queries for the search string within it. The result is a ```json``` object with scores as keys and a list of indices denoting where the substring is present in the DNA string. See Sample Output below.

### Sample Output:
```
{
score1: [[start, end], [start, end], [start, end], [start, end], [start, end]],
score2: [[start, end], [start, end], [start, end]],
score3: [[start, end], [start, end], [start, end], [start, end]],
score4: [[start, end], [start, end], [start, end], [start, end], [start, end], [start, end]],
}
```

### Team:
- Ali Haider
- Abuzar Rasool
- Asad Raza
- Faaz Abidi

### References:
- [GitHub](https://github.com/jojonki/FM-index)
- [Youtube](https://www.youtube.com/watch?v=kvVGj5V65io&t=1862s)
