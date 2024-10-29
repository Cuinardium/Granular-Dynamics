package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.*;

public class CellIndexMethod {

    private final int Mx;
    private final int My;
    private final double Lx;
    private final double Ly;

    private List<List<Set<Particle>>> grid;

    public CellIndexMethod(double length, double width, double  rc) {
        this.Lx = length;
        this.Ly = width;

        int Mx = (int) Math.floor(Lx/rc);

        if(Mx <= 0) {
            Mx = 1;
        }

        int My = (int) Math.floor(Ly/rc);

        if(My <= 0) {
            My = 1;
        }

        this.Mx = Mx;
        this.My = My;

        // M + 1 filas ( crece en x, es donde se presentan las condiciones periodicas de contorno)
        this.grid = new ArrayList<>(Mx+1);
        for(int i = 0; i < Mx; i++) {
            // M columnas
            this.grid.add(new ArrayList<>(My));
            // genero M HashSets
            for(int j = 0; j < My; j++) {
                this.grid.get(i).add (new HashSet<>());
            }
        }
        // copio la primer fila en la ultima
        this.grid.add(this.grid.get(0));
    }

    public Map<Particle, Set<Particle>> getNeighbours(List<Particle> particles) {
        Map<Particle, Set<Particle>> neighbours = new HashMap<>();
        // inicio todas las particulas
        particles.forEach(p -> neighbours.put(p, new HashSet<>()));

        clearGrid();
        updateGrid(particles);

        for (int x = 0; x < grid.size(); x++) {
            for (int y = 0; y < grid.get(x).size(); y++) {
                // dada la siguiente submatriz
                // A B C
                // D E F
                // G H I
                // estoy parado en E.
                Set<Particle> currentCellParticles = grid.get(x).get(y);
                for (Particle p1 : currentCellParticles) {
                    checkAdjacent(x, y, p1, neighbours);
                    // me saco a mi mismo
                    neighbours.get(p1).remove(p1);
                }
            }
        }
        return neighbours;
    }

    private static final int[][] NEIGHBOR_OFFSETS = {
        {0, 0}, {-1, 0}, {-1, 1}, {0, 1}, {1, 1}
    };
    
    private void checkAdjacent(int x, int y, Particle p1, Map<Particle, Set<Particle>> neighbours) {
        for (int[] offset : NEIGHBOR_OFFSETS) {
            int nx = x + offset[0];
            int ny = y + offset[1];
            if (nx >= 0 && ny >= 0 && nx < grid.size() && ny < grid.get(0).size()) {
                for (Particle p2 : grid.get(nx).get(ny)) {
                    neighbours.get(p1).add(p2);
                    neighbours.get(p2).add(p1);
                }
            }
        }
    }
    private void clearGrid() {
        for(List<Set<Particle>> row: grid) {
            for(Set<Particle> cell: row) {
                cell.clear();
            }
        }
    }

    private void updateGrid(List<Particle> particles) { 
        // agrego cada particula a su celda
        for(Particle p : particles) {
            // las que tienen pos negativa las pongo en la primera columna
            int x = (int) Math.max(0, ((p.getX() * Mx) / Lx));
            int y = (int) Math.max(0, ((p.getY() * My) / Ly));
            grid.get(x).get(y).add(p);
        }
    }
}
