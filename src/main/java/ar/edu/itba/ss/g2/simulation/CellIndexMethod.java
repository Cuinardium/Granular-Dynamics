package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.*;

public class CellIndexMethod {

    private final int M;
    private final int L;

    public CellIndexMethod(int M, int L) {
        this.M = M;
        this.L = L;
    }

    public Map<Particle, Set<Particle>> getNeighbours(Set<Particle> particles) {
        Map<Particle, Set<Particle>> map = new HashMap<>();

        List<List<Set<Particle>>> grid = generateGrid(particles);

        for(int x = 0; x < M; x++) {
            for(int y = 0; y < M; y++) {
                for(Particle p : grid.get(x).get(y)) {
                    checkAdjacent(x, y, grid, p, map);
                }
            }
        }

        return map;
    }

    private void addIfClose(Particle p1, Particle p2, Map<Particle, Set<Particle>> map) {
        if (p1.overlaps(p2)) {
            if (!map.containsKey(p1)) {
                map.put(p1, new HashSet<>());
            }
            if (!map.containsKey(p2)) {
                map.put(p2, new HashSet<>());
            }
            map.get(p1).add(p2);
            map.get(p2).add(p1);
        }
    }

    private void checkAdjacent(int x, int y, List<List<Set<Particle>>> grid, Particle p, Map<Particle, Set<Particle>> map) {
        if (x < 0 || y < 0 || x >= grid.size() || y >= grid.get(x).size()) {
            return;
        }

        // tengo
        // - - -
        // - x -
        // - - -

        // reviso
        // - x x
        // - x x
        // - - -
        for (int i = Math.max(x - 1, 0); i <= x; i++) {
            for (int j = y; j <= Math.min(y + 1, grid.size() - 1); j++) {
                for (Particle p2 : grid.get(i).get(j)) {
                    if (!p.equals(p2)) {
                        addIfClose(p, p2, map);
                    }
                }
            }
        }
        // reviso
        // - - -
        // - - -
        // - - x
        x = x + 1;
        y = y + 1;
        if (!(x >= grid.size() || y >= grid.get(x).size())) {
            for (Particle p2 : grid.get(x).get(y)) {
                if (!p.equals(p2)) {
                    addIfClose(p, p2, map);
                }
            }
        }
    }

    private List<List<Set<Particle>>> generateGrid(Set<Particle> particles) {
        List<List<Set<Particle>>> grid;

        // M + 1 filas ( crece en x, es donde se presentan las condiciones periodicas de contorno)
        grid = new ArrayList<>(M+1);
        for(int i = 0; i < M; i++) {
            // M columnas
            grid.add(new ArrayList<>(M));
            // genero M HashSets
            for(int j = 0; j < M; j++) {
                grid.get(i).add(new HashSet<>());
            }
        }
        // copio la primer fila en la ultima
        grid.set(M+1, grid.get(0));

        // agrego cada particula a su celda
        for(Particle p : particles) {
            // las que tienen pos negativa las pongo en la primera columna
            int x = (int) Math.max(0, ((p.getX() * M) / L));
            int y = (int) Math.max(0, ((p.getY() * M) / L));
            grid.get(x).get(y).add(p);
        }

        return grid;
    }
}
