// Done By Saif Battah - 1170986 @ 12/2/2023
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Function to generate a random number in the range [min, max]
int random_number(int min, int max) {
  return min + (rand() % (max - min + 1));
}

int main() {
  // Number of processes, max arrival time, and max number of CPU bursts
  int num_processes, max_arrival, max_cpu_bursts;

  // Min and max values for IO and CPU bursts
  int min_io, max_io, min_cpu, max_cpu;

  // Read the input values
  printf("Enter the number of processes: ");
  scanf("%d", &num_processes);
  printf("Enter the maximum arrival time: ");
  scanf("%d", &max_arrival);
  printf("Enter the maximum number of CPU bursts: ");
  scanf("%d", &max_cpu_bursts);
  printf("Enter the minimum IO burst duration: ");
  scanf("%d", &min_io);
  printf("Enter the maximum IO burst duration: ");
  scanf("%d", &max_io);
  printf("Enter the minimum CPU burst duration: ");
  scanf("%d", &min_cpu);
  printf("Enter the maximum CPU burst duration: ");
  scanf("%d", &max_cpu);

  // Seed the random number generator
  srand(time(NULL));

  // Open the output file
  FILE *f = fopen("workload.txt", "w");
  if (f == NULL) {
    printf("Error opening file!\n");
    return 1;
  }

  // Generate the workload and save it to the file
  for (int i = 0; i < num_processes; i++) {
    // Write the PID, arrival time, and CPU bursts to the file
    fprintf(f, "%d %d", i, random_number(0, max_arrival));
    int num_cpu_bursts = random_number(1, max_cpu_bursts);
    for (int j = 0; j < num_cpu_bursts; j++) {
      fprintf(f, " %d", random_number(min_cpu, max_cpu));
      if (j < num_cpu_bursts - 1) {
        fprintf(f, " %d", random_number(min_io, max_io));
      }
    }
    fprintf(f, "\n");
  }

  // Close the file
  fclose(f);

  return 0;
}
