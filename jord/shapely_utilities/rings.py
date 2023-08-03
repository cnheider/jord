from shapely import LinearRing


__all__ = ['ensure_ccw_ring','ensure_cw_ring']

def ensure_ccw_ring(ring: LinearRing)->LinearRing:
    if not ring.is_ccw:
        return LinearRing(list(ring.coords)[::-1])
    return ring


def ensure_cw_ring(ring: LinearRing)->LinearRing:
    if ring.is_ccw:
        return LinearRing(list(ring.coords)[::-1])
    return ring
