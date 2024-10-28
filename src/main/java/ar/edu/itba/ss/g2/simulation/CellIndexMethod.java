package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.*;

public class CellIndexMethod {

    private final int M;
    private final int L;
    private final double rc;

    public CellIndexMethod(int M, int L, double rc) {
        this.M = M;
        this.L = L;
        this.rc = rc;
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
