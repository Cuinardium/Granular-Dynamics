package ar.edu.itba.ss.g2.config;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;

import java.util.Comparator;
import java.util.List;

public class ArgParser {

    private static final List<Option> OPTIONS =
            List.of(
                    new Option("h", "help", false, "Print this message"),
                    new Option("W", "width", true, "Width of the environment"),
                    new Option("L", "length", true, "Length of the environment"),
                    new Option("M", "obstacle-count", true, "Number of obstacles"),
                    new Option("N", "particle-count", true, "Number of particles"),
                    new Option("R", "obstacle-radius", true, "Radius of the obstacles"),
                    new Option("r", "particle-radius", true, "Radius of the particles"),
                    new Option("m", "particle-mass", true, "Mass of the particles"),
                    new Option("A", "acceleration", true, "Acceleration of the particles"),
                    new Option("k_n", "normal-k", true, "Normal force constant"),
                    new Option("g", "gamma", true, "The amortiguator constant for the normal force"),
                    new Option("k_t", "tangential-k", true, "Tangential force constant"),
                    new Option("dt", "integration-step", true, "Integration step"),
                    new Option("dt2", "snapshot-step", true, "Snapshot step"),
                    new Option("tf", "max-time", true, "Max time"),
                    new Option("out", "output-directory", true, "Output directory"));

    private final String[] args;
    private final Options options;

    public ArgParser(String[] args) {
        this.args = args;

        Options options = new Options();
        OPTIONS.forEach(options::addOption);
        this.options = options;
    }

    public Config parse() {

        CommandLineParser parser = new DefaultParser();

        CommandLine cmd;

        try {
            cmd = parser.parse(options, args);
        } catch (Exception e) {
            System.err.println("Error parsing arguments: " + e.getMessage());
            return null;
        }

        if (cmd.hasOption("h")) {
            return null;
        }

        Config.Builder builder = new Config.Builder();

        // width
        if (cmd.hasOption("W")) {
            double width;

            try {
                width = Double.parseDouble(cmd.getOptionValue("W"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Width: " + cmd.getOptionValue("W"));
                return null;
            }

            if (width <= 0) {
                System.err.println("Invalid Width: " + cmd.getOptionValue("W"));
                return null;
            }

            builder.width(width);
        } else {
            System.err.println("Width (W) is required");
            return null;
        }

        // length
        if (cmd.hasOption("L")) {
            double length;

            try {
                length = Double.parseDouble(cmd.getOptionValue("L"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Length: " + cmd.getOptionValue("L"));
                return null;
            }

            if (length <= 0) {
                System.err.println("Invalid Length: " + cmd.getOptionValue("L"));
                return null;
            }

            builder.length(length);
        } else {
            System.err.println("Length (L) is required");
            return null;
        }

        // obstacle-count
        if (cmd.hasOption("M")) {
            int obstacleCount;

            try {
                obstacleCount = Integer.parseInt(cmd.getOptionValue("M"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Obstacle Count: " + cmd.getOptionValue("M"));
                return null;
            }

            if (obstacleCount <= 0) {
                System.err.println("Invalid Obstacle Count: " + cmd.getOptionValue("M"));
                return null;
            }

            builder.obstacleCount(obstacleCount);
        } else {
            System.err.println("Obstacle count (M) is required");
            return null;
        }

        // particle-count
        if (cmd.hasOption("N")) {
            int particleCount;

            try {
                particleCount = Integer.parseInt(cmd.getOptionValue("N"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Particle Count: " + cmd.getOptionValue("N"));
                return null;
            }

            if (particleCount <= 0) {
                System.err.println("Invalid Particle Count: " + cmd.getOptionValue("N"));
                return null;
            }

            builder.particleCount(particleCount);
        } else {
            System.err.println("Particle Count (N) is required");
            return null;
        }

        // obstacle-radius
        if (cmd.hasOption("R")) {
            double obstacleRadius;

            try {
                obstacleRadius = Double.parseDouble(cmd.getOptionValue("R"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Obstacle Radius: " + cmd.getOptionValue("R"));
                return null;
            }

            if (obstacleRadius <= 0) {
                System.err.println("Invalid Obstacle Radius: " + cmd.getOptionValue("R"));
                return null;
            }

            builder.obstacleRadius(obstacleRadius);
        } else {
            System.err.println("Obstacle Radius (R) is required");
            return null;
        }

        // particle-radius
        if (cmd.hasOption("r")) {
            double particleRadius;

            try {
                particleRadius = Double.parseDouble(cmd.getOptionValue("r"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Particle Radius: " + cmd.getOptionValue("r"));
                return null;
            }

            builder.particleRadius(particleRadius);
        } else {
            System.err.println("Particle radius (r) is required");
            return null;
        }

        // acceleration
        if (cmd.hasOption("A")) {
            double acceleration;

            try {
                acceleration = Double.parseDouble(cmd.getOptionValue("A"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Acceleration: " + cmd.getOptionValue("A"));
                return null;
            }

            builder.acceleration(acceleration);
        } else {
            System.err.println("Acceleration (A) is required");
            return null;
        }

        // particle-mass
        if (cmd.hasOption("m")) {
            double particleMass;

            try {
                particleMass = Double.parseDouble(cmd.getOptionValue("m"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Particle Mass: " + cmd.getOptionValue("m"));
                return null;
            }

            builder.particleMass(particleMass);
        } else {
            System.err.println("Particle mass (m) is required");
            return null;
        }

        // normal-k
        if (cmd.hasOption("k_n")) {
            double normalK;

            try {
                normalK = Double.parseDouble(cmd.getOptionValue("k_n"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Normal K: " + cmd.getOptionValue("k_n"));
                return null;
            }

            builder.normalK(normalK);
        } else {
            System.err.println("Normal K (k_n) is required");
            return null;
        }

        // gamma
        if (cmd.hasOption("g")) {
            double gamma;

            try {
                gamma = Double.parseDouble(cmd.getOptionValue("g"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Gamma: " + cmd.getOptionValue("g"));
                return null;
            }

            builder.gamma(gamma);
        } else {
            System.err.println("Gamma (g) is required");
            return null;
        }

        // tangential-k
        if (cmd.hasOption("k_t")) {
            double tangentialK;

            try {
                tangentialK = Double.parseDouble(cmd.getOptionValue("k_t"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Tangential K: " + cmd.getOptionValue("k_t"));
                return null;
            }

            builder.tangentialK(tangentialK);
        } else {
            System.err.println("Tangential K (k_t) is required");
            return null;
        }

        // integration-step
        if (cmd.hasOption("dt")) {
            double integrationStep;

            try {
                integrationStep = Double.parseDouble(cmd.getOptionValue("dt"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Integration Step: " + cmd.getOptionValue("dt"));
                return null;
            }

            builder.integrationStep(integrationStep);
        } else {
            System.err.println("Integration Step (dt) is required");
            return null;
        }

        // snapshot-step
        if (cmd.hasOption("dt2")) {
            double snapshotStep;

            try {
                snapshotStep = Double.parseDouble(cmd.getOptionValue("dt2"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Snapshot Step: " + cmd.getOptionValue("dt2"));
                return null;
            }

            builder.snapshotStep(snapshotStep);
        } else {
            System.err.println("Snapshot Step (dt2) is required");
            return null;
        }

        // max-time
        if (cmd.hasOption("tf")) {
            double maxTime;

            try {
                maxTime = Double.parseDouble(cmd.getOptionValue("tf"));
            } catch (NumberFormatException e) {
                System.err.println("Invalid Max Time: " + cmd.getOptionValue("tf"));
                return null;
            }

            builder.maxTime(maxTime);
        } else {
            System.err.println("Max Time (tf) is required");
            return null;
        }

        // output-dir
        if (cmd.hasOption("out")) {
            builder.outputDirectory(cmd.getOptionValue("out"));
        } else {
            System.err.println("Output Directory is required");
            return null;
        }

        return builder.build();
    }

    public void printHelp() {

        HelpFormatter formatter = new HelpFormatter();
        formatter.setOptionComparator(Comparator.comparingInt(OPTIONS::indexOf));

        formatter.setLeftPadding(4);
        formatter.setWidth(120);

        String commandLineSyntax =
                "java -jar granullar-dynamics-1.0-jar-with-dependencies.jar [options]";

        formatter.printHelp(commandLineSyntax, options);
    }
}
