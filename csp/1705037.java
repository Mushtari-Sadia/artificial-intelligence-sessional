import org.chocosolver.solver.Model;
import org.chocosolver.solver.Solver;
import org.chocosolver.solver.variables.IntVar;


public class Sudoku {
public static void main(String[] args) {


int i, j, k;


// 1. Create a Model
Model model = new Model("my first sudoku problem");
// 2. Create variables



/* the board which is 9 X 9 */
/* (0, 0) is the top left position and (8, 8) is the bottom right position */
/*each cell is an integer variable taking their value in [1, 9] */
IntVar[][] bd = model.intVarMatrix("bd", 6, 6, 1, 6);


 /* the nine rows */
 /* each row is an array of 9 integer variables taking their value in [1, 9] */
IntVar[] r0 = model.intVarArray("r0", 6, 1, 6);
IntVar[] r1 = model.intVarArray("r1", 6, 1, 6);
IntVar[] r2 = model.intVarArray("r2", 6, 1, 6);
IntVar[] r3 = model.intVarArray("r3", 6, 1, 6);
IntVar[] r4 = model.intVarArray("r4", 6, 1, 6);
IntVar[] r5 = model.intVarArray("r5", 6, 1, 6);


/* the nine columns */
/* each column is an array of 9 integer variables taking their value in [1, 9] */

IntVar[] c0 = model.intVarArray("c0", 6, 1, 6);
IntVar[] c1 = model.intVarArray("c1", 6, 1, 6);
IntVar[] c2 = model.intVarArray("c2", 6, 1, 6);
IntVar[] c3 = model.intVarArray("c3", 6, 1, 6);
IntVar[] c4 = model.intVarArray("c4", 6, 1, 6);
IntVar[] c5 = model.intVarArray("c5", 6, 1, 6);

/* the nine blocks or boxes */
/* each box is an array of 9 integer variables taking their value in [1, 9] */


// 3. Post constraints


/* post constraints for the given hints or clues */



model.sum(new IntVar[]{bd[0][0],bd[1][0], bd[2][0]}, "=", 8).post();
model.sum(new IntVar[]{bd[0][4],bd[0][5], bd[1][5]}, "=", 10).post();
model.sum(new IntVar[]{bd[2][1],bd[3][1], bd[4][1]}, "=", 12).post();
model.sum(new IntVar[]{bd[2][2],bd[2][3]}, "=", 8).post();


model.arithm(bd[0][1].mul(bd[0][2], bd[0][3]).intVar(), "=", 36).post();
model.arithm(bd[1][3].mul(bd[1][4]).intVar(), "=", 30).post();
model.arithm(bd[3][3].mul(bd[4][3]).intVar(), "=", 6).post();
model.arithm(bd[4][5].mul(bd[5][5]).intVar(), "=", 30).post();

model.arithm(bd[2][5].sub(bd[3][5]).abs().intVar(), "=", 1).post();
model.arithm(bd[3][0].sub(bd[4][0]).abs().intVar(), "=", 1).post();
model.arithm(bd[3][2].sub(bd[4][2]).abs().intVar(), "=", 3).post();
model.arithm(bd[5][0].sub(bd[5][1]).abs().intVar(), "=", 3).post();
model.arithm(bd[5][2].sub(bd[5][3]).abs().intVar(), "=", 1).post();

model.arithm(bd[1][1].max(bd[1][2]).intVar(), "=", bd[1][1].min(bd[1][2]).mul(2).intVar()).post();
model.arithm(bd[2][4].max(bd[3][4]).intVar(), "=", bd[2][4].min(bd[3][4]).mul(2).intVar()).post();
model.arithm(bd[4][4].max(bd[5][4]).intVar(), "=", bd[4][4].min(bd[5][4]).mul(3).intVar()).post();


/* for the nine box variables */
/* each box variable is associated with appropriate cell positions in board */
/* for example, b0 [0] is equal to board [0][0] and b0 [8] is equal to board [3][3] */
/* b1 [0] is equal to board [0][3] and b1 [8] is equal to board [2][5] */
/* b2 [0] is equal to board [0][6] and b2 [8] is equal to board [2][8] */
/* Continuing in this way, b8 [8] is equal to board [8][8] */

    
/* for the nine row variables */
/* each row variable is associated with appropriate cell positions in board */
    
for ( j = 0; j < 6; j++)
  model.arithm (bd[0][j], "=", r0[j]).post();
  
for ( j = 0; j < 6; j++)
  model.arithm (bd[1][j], "=", r1[j]).post();
    
for ( j = 0; j < 6; j++)
  model.arithm (bd[2][j], "=", r2[j]).post();

for ( j = 0; j < 6; j++)
  model.arithm (bd[3][j], "=", r3[j]).post();
  
for ( j = 0; j < 6; j++)
  model.arithm (bd[4][j], "=", r4[j]).post();
    
for ( j = 0; j < 6; j++)
  model.arithm (bd[5][j], "=", r5[j]).post();
  




/* for the nine column variables */
/* each column variable is associated with appropriate cell positions in board */


for ( i = 0; i < 6; i++)
  model.arithm (bd[i][0], "=", c0[i]).post();

for ( i = 0; i < 6; i++)
  model.arithm (bd[i][1], "=", c1[i]).post();

for ( i = 0; i < 6; i++)
  model.arithm (bd[i][2], "=", c2[i]).post();

for ( i = 0; i < 6; i++)
  model.arithm (bd[i][3], "=", c3[i]).post();

for ( i = 0; i < 6; i++)
  model.arithm (bd[i][4], "=", c4[i]).post();

for ( i = 0; i < 6; i++)
  model.arithm (bd[i][5], "=", c5[i]).post();




/* post global constraint alldiff for the nine rows */

model.allDifferent(r0).post();
model.allDifferent(r1).post();
model.allDifferent(r2).post();
model.allDifferent(r3).post();
model.allDifferent(r4).post();
model.allDifferent(r5).post();




/* post global constraint alldiff for the nine columns */

model.allDifferent(c0).post();
model.allDifferent(c1).post();
model.allDifferent(c2).post();
model.allDifferent(c3).post();
model.allDifferent(c4).post();
model.allDifferent(c5).post();





/* post global constraint alldiff for the nine boxes */







// 4. Solve the problem




     Solver solver = model.getSolver();

    solver.showStatistics();
    solver.showSolutions();
    solver.findSolution();


// 5. Print the solution

for ( i = 0; i < 6; i++)
    {
for ( j = 0; j < 6; j++)
     { 
  
        System.out.print(" "); 
        /* get the value for the board position [i][j] for the solved board */
        k = bd [i][j].getValue();
        System.out.print(k );
     }
     System.out.println();
    }


}

}

