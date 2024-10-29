package ar.edu.itba.ss.g2.simulation;

import ar.edu.itba.ss.g2.model.Particle;

import java.util.*;

public class CellIndexMethod {

    private final int Mx;
    private final int My;
    private final double Lx;
    private final double Ly;

    private final Set<Particle>[][] grid;


    public CellIndexMethod(double length, double width, double  rc) {
        this.Lx = length;
        this.Ly = width;
        this.Mx = (int) Math.max(1, Math.floor(Lx/rc));
        this.My = (int) Math.max(1, Math.floor(Ly/rc));

        this.grid = new HashSet[Mx+1][My];

        for (int i = 0; i < Mx; i++) {
            for (int j = 0; j < My; j++) {
                grid[i][j] = new HashSet<>();
            }
        }

        // copio la primer fila en la ultima
        this.grid[Mx] = this.grid[0];
    }

    public Map<Particle, Set<Particle>> getNeighbours(List<Particle> particles) {
        Map<Particle, Set<Particle>> neighbours = new HashMap<>();
        // inicio todas las particulas
        particles.forEach(p -> neighbours.put(p, new HashSet<>()));

        clearGrid();
        updateGrid(particles);

        for (int x = 0; x < Mx + 1; x++) {
            for (int y = 0; y < My; y++) {
                // dada la siguiente submatriz
                // A B C
                // D E F
                // G H I
                // estoy parado en E.
                Set<Particle> currentCellParticles = grid[x][y];
                for (Particle p1 : currentCellParticles) {
                    checkAdjacent(x, y, p1, neighbours);
                    // me saco a mi mismo
                    neighbours.get(p1).remove(p1);
                }
            }
        }
        return neighbours;
    }

    private static final int[][] NEIGHBOUR_OFFSETS = {
        {0, 0}, {-1, 0}, {-1, 1}, {0, 1}, {1, 1}
    };
    
    private void checkAdjacent(int x, int y, Particle p1, Map<Particle, Set<Particle>> neighbours) {
        for (int[] offset : NEIGHBOUR_OFFSETS) {
            int nx = x + offset[0];
            int ny = y + offset[1];
            if (nx >= 0 && ny >= 0 && nx < Mx+1 && ny < My) {
                for (Particle p2 : grid[nx][ny]) {
                    neighbours.get(p1).add(p2);
                    neighbours.get(p2).add(p1);
                }
            }
        }
    }
    private void clearGrid() {
        
        for(Set<Particle>[] row: grid) {
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
            grid[x][y].add(p);
        }
    }
}
