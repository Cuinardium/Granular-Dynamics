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
        int Mx = (int) Math.floor(length/rc);

        if(Mx <= 0) {
            Mx = 1;
        }

        int My = (int) Math.floor(width/rc);

        if(My <= 0) {
            My = 1;
        }

        this.Mx = Mx;
        this.My = My;
        this.Lx = length;
        this.Ly = width;
    }

    public Map<Particle, Set<Particle>> getNeighbours(List<Particle> particles) {
        Map<Particle, Set<Particle>> neighbours = new HashMap<>();
        // inicio todas las particulas
        particles.forEach(p -> neighbours.put(p, new HashSet<>()));

        grid = generateGrid(particles);

        for (int x = 0; x < grid.size(); x++) {
            for (int y = 0; y < grid.get(x).size(); y++) {
                // dada la siguiente submatriz
                // A B C
                // D E F
                // G H I
                // estoy parado en E.
                Set<Particle> currentCellParticles = grid.get(x).get(y);
                for (Particle p1 : currentCellParticles) {
                    // reviso E
                    checkAdjacent(x, y, p1, neighbours);
                    // me saco a mi mismo
                    neighbours.get(p1).remove(p1);

                    // reviso B
                    checkAdjacent(x - 1, y, p1, neighbours);
                    // reviso C
                    checkAdjacent(x - 1, y+1, p1, neighbours);
                    // reviso F
                    checkAdjacent(x, y+1, p1, neighbours);
                    // reviso I
                    checkAdjacent(x+1 , y+1, p1, neighbours);
                }
            }
        }
        return neighbours;
    }

    private void checkAdjacent(int x, int y, Particle p1, Map<Particle, Set<Particle>> neighbours) {
        if(x < 0 || y < 0 || x >= grid.size() || y >= grid.get(0).size()) {
            return;
        }
        Set<Particle> adjacentCellParticles = grid.get(x).get(y);
        for(Particle p2: adjacentCellParticles) {
            neighbours.get(p1).add(p2);
             neighbours.get(p2).add(p1);
        }
    }

    private List<List<Set<Particle>>> generateGrid(List<Particle> particles) {
        List<List<Set<Particle>>> grid;

        // M + 1 filas ( crece en x, es donde se presentan las condiciones periodicas de contorno)
        grid = new ArrayList<>(Mx+1);
        for(int i = 0; i < Mx; i++) {
            // M columnas
            grid.add(new ArrayList<>(My));
            // genero M HashSets
            for(int j = 0; j < My; j++) {
                grid.get(i).add (new HashSet<>());
            }
        }
        // copio la primer fila en la ultima
        grid.add(grid.get(0));

        // agrego cada particula a su celda
        for(Particle p : particles) {
            // las que tienen pos negativa las pongo en la primera columna
            int x = (int) Math.max(0, ((p.getX() * Mx) / Lx));
            int y = (int) Math.max(0, ((p.getY() * My) / Ly));
            grid.get(x).get(y).add(p);
        }

        return grid;
    }
}
