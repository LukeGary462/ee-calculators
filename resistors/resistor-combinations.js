<script type="text/javascript">
//<![CDATA[

  /* Copyright (C) 2001-2010 Claudio Girardi
   *
   * This program is free software; you can redistribute it and/or modify
   * it under the terms of the GNU General Public License as published by
   * the Free Software Foundation; either version 2 of the License, or (at
   * your option) any later version.
   *
   * This program is distributed in the hope that it will be useful, but
   * WITHOUT ANY WARRANTY; without even the implied warranty of
   * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   * General Public License for more details.
   *
   * You should have received a copy of the GNU General Public License
   * along with this program; if not, write to the Free Software
   * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
   */

    /* well, this is not the simplest way to do it but, as they say, */
    /* If ain't broke, don't fix it!"                                */


   function select_series() {
     var sel_val = document.getElementById('rslist').options[document.getElementById('rslist').selectedIndex].value;
     switch(sel_val) {
       case "E12":
         Rbase = new Array(1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2);
         break;
       case "E24":
        Rbase = new Array(1, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1);
        break;
       case "E96":
        Rbase = new Array(1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49, 5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76);
         break;
       default:
     }


     R = new Array;
     for (var mult = 0; mult <= 6; mult++) {
       for (var idx = 0; idx <Rbase.length; idx++) {
         /* need to round to compensate for pow() errors; allow max two decimals, needed for E96 */
         R[idx + mult * Rbase.length] = Math.round(Rbase[idx] * Math.pow(10, mult) * 100) / 100;
       }
     }
     n_max = R.length - 1; /* maximum valid index */

     /* compute the conductances array, lowest conductance first to have an */
     /* array sorted in ascending order */
     G = new Array;
     for (idx = 0; idx <= n_max; idx++) {
       G[idx] = 1.0 / R[n_max - idx];
     }

     out_r1 = new Array;
     out_r2 = new Array;
     out_op = new Array;
     out_rres = new Array;
     out_tol = new Array;

     CalcRes();
   }


    function FindIndex(vect, value) {
      var index_min = 0;
      var index_max = n_max + 1;
      var index = Math.floor( (index_min + index_max) / 2);
      i = 0;

      while (((index_max - index_min) > 1) && (i < 500)) {
        if (vect[index] == value) { break; }
        else if (vect[index] > value) { index_max = index }
        else if (vect[index] < value) { index_min = index }

        index = Math.floor( (index_min + index_max) / 2);
        i++;
      }
      if (index < n_max) {
        tol1 = Math.abs(vect[index] / value - 1.0);
        tol2 = Math.abs(vect[index + 1] / value - 1.0);
        if (tol1 < tol2)
          return index;
        else
          return (index + 1);
      } else
        return index;
    }

    function CalcRes() {
      var rd = document.getElementById('rd').value;
      var r1, r2, r1_idx, rres, rres_tol, best_tol, out_idx, op;
      var out_prres, out_vrres;
      var i, j, iter = 0; /* number of iterations */

      document.getElementById('texta').value = ""
<!--      document.getElementById('debuga').value = "" -->

      /* compute assuming resistors in series */
      /* locate nearest approximation with standard resistor values */
      r1_idx = FindIndex(R, rd);
      r1 = R[r1_idx];
      /* other resistor */
      /* r2 = Number.POSITIVE_INFINITY */
      r2 = 0;
      rres = r1;
      rres_tol = (rres - rd) / rd; /* relative tolerance */
      best_tol = rres_tol;

      out_idx = 0;
      out_r1[out_idx] = r1;
      out_r2[out_idx] = r2;
      out_op[out_idx] = "+";
      out_rres[out_idx] = rres;
      out_tol[out_idx++] = rres_tol;

      for (; R[r1_idx] >= rd / 2.0; r1_idx--) {
        iter++;
        r1 = R[r1_idx];

        r2d = rd - r1; // this is the value needed
<!--        document.getElementById('debuga').value += '+ ' + rd + ' ' + r1 + ' ' + r2d + ' ' + 1/rd + ' ' + 1/r1 + ' ' + 1/r2d + '\n' -->
        if (r2d < 0) { continue } // might happen...

        r2_idx = FindIndex(R, r2d);
        r2 = R[r2_idx];  // get the nearest standard value
        rres = r1 + r2; // compute the resulting composition
        rres_tol = rres / rd - 1.0; // and its tolerance


        if (Math.abs(rres_tol) < Math.abs(best_tol)) {
          //best_tol = rres_tol;
          out_r1[out_idx] = r1;
          out_r2[out_idx] = r2;
          out_op[out_idx] = "+";
          out_rres[out_idx] = rres;
          out_tol[out_idx++] = rres_tol;
        }

      }

      rd = 1.0 / rd;
      /* compute assuming resistors in parallel */
      r1_idx = FindIndex(G, rd);
      for (; G[r1_idx] >= rd / 2.1; r1_idx--) {
        iter++;
        r1 = G[r1_idx];

        r2d = rd - r1; // this is the value needed
<!--         document.getElementById('debuga').value += '|| ' + rd + ' ' + r1 + ' ' + r2d + ' ' + 1/rd + ' ' + 1/r1 + ' ' + 1/r2d + '\n' -->
        if (r2d < 0) { continue } // might happen...

        r2_idx = FindIndex(G, r2d);
        r2 = G[r2_idx];  // get the nearest standard value
        rres = r1 + r2; // compute the resulting composition
        rres_tol = rd / rres - 1.0; // and its tolerance

        if (Math.abs(rres_tol) < Math.abs(best_tol)) {
          //best_tol = rres_tol;
          // use values from R array to avoid rounding errors
          //   which will lead to something like 6800.0000001...
          out_r1[out_idx] = R[n_max - r1_idx] // 1.0 / r1;
          out_r2[out_idx] = R[n_max - r2_idx] // 1.0 / r2;
          out_op[out_idx] = "||";
          out_rres[out_idx] = 1.0 / rres;
          out_tol[out_idx++] = rres_tol;
        }
      }

      // sort the results
      for (i = 1; i < out_idx; i++) {
        r1 = out_r1[i];
        r2 = out_r2[i];
        op = out_op[i];
        rres = out_rres[i];
        rres_tol = out_tol[i];
        for (j = i - 1; (j >= 0) &&
             Math.abs(out_tol[j]) > Math.abs(rres_tol); j--) {
          out_r1[j + 1] = out_r1[j];
          out_r2[j + 1] = out_r2[j];
          out_op[j + 1] = out_op[j];
          out_rres[j + 1] = out_rres[j];
          out_tol[j + 1] = out_tol[j];
        }
        out_r1[j + 1] = r1;
        out_r2[j + 1] = r2;
        out_op[j + 1] = op;
        out_rres[j + 1] = rres;
        out_tol[j + 1] = rres_tol;
      }

      for (r1_idx = 0; r1_idx < out_idx; r1_idx++) {
        out_prres = (Math.round(out_rres[r1_idx] * 1000)) / 1000 ;
        out_vrres = out_prres.toString();
        if(out_vrres.length < 8) out_vrres = out_vrres + "\t"
        document.getElementById('texta').value +=
          out_r1[r1_idx] + "\t" +
          out_op[r1_idx] + "\t" +
          out_r2[r1_idx] + "\t=\t" +
          /* leave three decimal digits maximum */
          out_vrres + "\t(" +
          (Math.round(out_tol[r1_idx] * 100000)) / 1000 + " %)\n"
      }
    // put the focus on the input field
    //document.getElementById('rd').focus();

    }

//]]>
</script>