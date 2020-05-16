from gene import Gene
from math import pi

# A biomorph is nothing more than a
# collection of genes
# The genes control its appearance.
class Biomorph:
    def __init__(self):
        # Create the genes
        # The number of iterations to go through - the number of times to branch
        # nine discrete values from 1 to 9 (step of 1)
        self.iterations = Gene('Iterations', 1, 9, 9)

        # The branching lengths for branches pointing 'upwards'  and downwards
        # from -30 to 30 (step of 0.2)
        self.branch_length_up = Gene('Branch length (up)', -30, 30, 51)
        self.branch_length_down  = Gene('Branch length (down)', -30, 30, 51)

        # The branching angles for branches pointing 'upwards' (-pi/2 -> 3/4 pi/2) and downwards
        self.branch_angle_up = Gene('Branch angle (up)', -pi, .75 * pi, 16)
        self.branch_angle_down = Gene('Branch angle (down)', -pi, 0.75 * pi, 16)

        # How much to change the length of a branch pointing 'upwards' and 'downwards'
        self.branch_length_delta_up = Gene('Branch length delta (up)', -30, 30, 31);
        self.branch_length_delta_down = Gene('Branch length delta (down)', -30, 30, 31);

        # How much to change the angles of branches pointing 'upwards' and 'downwards'
        self.branch_angle_delta_up = Gene('Branch angle delta (up)', -pi, 0.75 * pi, 16);
        self.branch_angle_delta_down = Gene('Branch angle delta (down)', -pi, 0.75 * pi, 16);

        # The aspect ratio - width / height that scales stretches and squashes the biomorph
        self.aspect_ratio = Gene('Aspect ratio', 0.2, 5, 25)

        # And a list of all genes for ease of manipulation
        self.all_genes = [self.iterations,
                          self.branch_length_up, self.branch_length_down,
                          self.branch_angle_up, self.branch_angle_down,
                          self.branch_length_delta_up, self.branch_length_delta_down,
                          self.branch_angle_delta_up, self.branch_angle_delta_down,
                          self.aspect_ratio]

    # Randomise all the genes
    def randomise(self):
        for gene in self.all_genes:
            gene.randomise()

    # Clone the biomorph by creating a new one and copying all the gene values
    def clone(self):
        clone = Biomorph()
        for (geneA, geneB) in zip (self.all_genes, clone.all_genes):
            geneB.underlying_value = geneA.underlying_value
        return clone

    # Generate offspring
    # We create two clones of the biomorph for each gene (one with the value increased, one with the value decreased).
    # Thus the offspring remain closely 'related' to their parent.
    # In total we create 2 * the number of genes offspring
    def generate_offspring_standard(self):
        offspring = []
        for index, gene in enumerate(self.all_genes):
            clone_up = self.clone()
            clone_up.all_genes[index].increment()
            offspring.append((clone_up))
            clone_down = self.clone()
            clone_down.all_genes[index].decrement()
            offspring.append((clone_down))
        return offspring

