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

    private List<List<Set<Particle>>> generateGrid(Set<Particle> particles) {
        List<List<Set<Particle>>> grid;

        // M filas
        grid = new ArrayList<>(M);
        for(int i = 0; i < M; i++) {
            // M + 1 columnas (condiciones periodicas de contorno)
            grid.add(new ArrayList<>(M+1));
            // genero M HashSets
            for(int j = 0; j < M; j++) {
                grid.get(i).add(new HashSet<>());
            }
            // copio el 0 en el M+1
            grid.set(M+1, grid.get(0));
        }

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
