# geohash-on-steroids
I'm making this repository for geohashing enthusiasts who want to encode and decode geohashes in the most python-optimized way.
I'll be experimenting more and adding more fuctionalities very soon.

## Dependencies
Optimized functions are created with the `njit` decorators and using arrays so the only dependencies are [Numba](https://github.com/numba/numba) and [Numpy](https://github.com/numpy/numpy).

## Performance
As you can see in my [notebook](https://github.com/IlyasMoutawwakil/geohash-on-steroids/blob/main/performance_tests.ipynb), performance gain in comparison to what's on the python package [pygeohash](https://github.com/wdm0006/pygeohash) is the following:

```python
%%timeit
point_decode(geohash)
# Output: 20.4 µs ± 367 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

```python
%%timeit
nb_point_decode(geohash)
# Output: 4.48 µs ± 16.8 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
```

```python
%%timeit
point_encode(latitude, longitude)
# Output: 92.8 µs ± 2.37 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

```python
%%timeit
nb_point_encode(latitude, longitude)
# Output: 11.2 µs ± 663 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
```
But geohashing is generally performaded on large amounts of data points so I made a vector-wise implimentation that perform well at large scale:

```python
%%timeit
np_vector_decode(geohashes)
# Output: 2.09 s ± 25.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

```python
%%timeit
nb_vector_decode(geohashes)
# Output: 164 ms ± 1.66 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

```python
%%timeit
np_vector_encode(latitudes, longitudes)
# Output: 2.57 s ± 53.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

```python
%%timeit
nb_vector_encode(latitudes, longitudes)
# Output: 443 ms ± 12.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```
## Roadmap
- [x] Use Numba for computing efficient geohash encoding and decoding
- [x] Use Numba for computing efficient geohash decoding
- [x] Use Numba for vector-wize computing efficient geohash encoding
- [x] Use Numba for vector-wize computing efficient geohash decoding
- [ ] Parallelize computations efficiently (one loop? no loops?)
