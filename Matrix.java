import java.lang.IndexOutOfBoundsException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Collections;

/*
 * Reads a matrix from stdin, reduces its bandwith using the Reverse CutHill-McKee algorithm and outputs to stdout
 * The matrix is represented as a graph adjacency list - each line giving connected node indexes (starting with 1) separated by blanks
 */

class Matrix {
	ArrayList<ArrayList<Integer>> adjacencyList = null;

	public Matrix () {
		adjacencyList = new ArrayList<ArrayList<Integer>> ();
	}

	public void loadMatrix () throws InvalidMatrixException {
		BufferedReader r = new BufferedReader (new InputStreamReader (System.in));
		String line = null;

		// So we can index starting from 1
		adjacencyList.add (null);

		try {
			while ((line = r.readLine ()) != null) {
				ArrayList<Integer> adj = new ArrayList<Integer> ();

				// So we can index starting from 1
				adj.add (-1);

				Scanner s = new Scanner (line);

				while (s.hasNextInt ()) {
					adj.add (s.nextInt ());
				}

				adjacencyList.add (adj);
			}
		} catch (IOException e) {
			throw new InvalidMatrixException ("Error reading matrix");
		}
	}

	public void printMatrix () {
		for (ArrayList<Integer> list : adjacencyList) {
			if (list == null)
				continue;

			for (Integer node : list) {
				if (node == -1)
					continue;

				System.out.printf ("%d ", node);
			}

			System.out.println ();
		}
	}

	private ArrayList<ArrayList<Integer>> copyAdjacencyList () {
		ArrayList<ArrayList<Integer>> list = new ArrayList<ArrayList<Integer>> ();

		for (ArrayList<Integer> l : adjacencyList) {
			if (l == null)
				list.add (null);
			else {
				ArrayList<Integer> row = new ArrayList<Integer> ();
				row.addAll (l);
				list.add (row);
			}
		}

		return list;
	}

	private void ensureSquare () {
		int maxNode = -1;

		for (ArrayList<Integer> list : adjacencyList) {
			if (list == null)
				continue;

			for (Integer node : list) {
				if (node > maxNode)
					maxNode = node;
			}
		}

		while (maxNode + 1 < adjacencyList.size ()) {
			ArrayList<Integer> newList = new ArrayList<Integer> ();

			adjacencyList.add (newList);
		}
	}

	private void makeSymmetric () {
		for (int i = 1; i < adjacencyList.size (); i++) {
			ArrayList<Integer> list = adjacencyList.get (i);

			for (int j = 1; j < list.size (); j++) {
				int node = list.get (j);
				ArrayList<Integer> transposeList = adjacencyList.get (node);

				if (!transposeList.contains (i)) {
					transposeList.add (i);
				}
			}
		}
	}

	public void reduceBandwidth () throws InvalidMatrixException {
		ArrayList<ArrayList<Integer>> origAdj = copyAdjacencyList ();

		ensureSquare ();
		makeSymmetric ();

		if (!isSymmetric ())
			throw new InvalidMatrixException ("Matrix not symmetric");

		ArrayList<Integer> results = new ArrayList<Integer> ();
		ArrayList<Integer> queue = new ArrayList<Integer> ();

		while (true) {
			int minDegree = -1;

			for (int i = 1; i < adjacencyList.size (); i++) {
				if (results.contains (i))
					continue;

				if (minDegree == -1 || adjacencyList.get (i).size () < adjacencyList.get (minDegree).size ())
					minDegree = i;
			}

			if (minDegree == -1)
				break;

			results.add (minDegree);

			queue = getUnprocessedAdjacencies (minDegree, results, queue);

			while (!queue.isEmpty ()) {
				int node = queue.remove (0);
				results.add (node);

				queue.addAll (getUnprocessedAdjacencies (node, results, queue));
			}
		}

		Collections.reverse (results);

		// Now renumber the nodes in the list

		ArrayList<ArrayList<Integer>> newAdjacencyList = new ArrayList<ArrayList<Integer>> (origAdj.size ());
		newAdjacencyList.add (null);

		for (int i = 1; i < origAdj.size (); i++) {
			ArrayList<Integer> list = origAdj.get (i);

			for (int j = 1; j < list.size (); j++) {
				int newIndex = results.indexOf (list.get (j)) + 1;

				list.set (j, newIndex);
			}

			Collections.sort (list);

			newAdjacencyList.add (null);
		}


		for (int i = 1; i < newAdjacencyList.size (); i++) {
			int newIndex = results.indexOf (i) + 1;

			newAdjacencyList.set (newIndex, origAdj.get (i));
		}

		adjacencyList = newAdjacencyList;
	}

	private ArrayList<Integer> getUnprocessedAdjacencies (int node, ArrayList<Integer> results, ArrayList<Integer> queue) {
		ArrayList<Integer> res = new ArrayList<Integer> ();

		for (Integer adjNode : adjacencyList.get (node)) {
			if (adjNode == -1)
				continue;

			if (results.contains (adjNode))
				continue;

			if (queue.contains (adjNode))
				continue;

			int insertAt = 0;
			int degree = adjacencyList.get (adjNode).size ();

			for (; insertAt < res.size (); insertAt++) {
				int curDegree = adjacencyList.get (res.get (insertAt)).size ();

				if (curDegree > degree)
					break;
			}

			res.add (insertAt, adjNode);
		}

		return res;
	}

	public boolean isSymmetric () {
		for (int i = 1; i < adjacencyList.size (); i++) {
			ArrayList<Integer> list = adjacencyList.get (i);

			for (int j = 1; j < list.size (); j++) {
				int node = list.get (j);

				try {
					if (!adjacencyList.get (node).contains (i)) {
						return false;
					}
				} catch (IndexOutOfBoundsException e) {
					return false;
				}
			}
		}

		return true;
	}

	public static void main (String[] args) {
		Matrix m = new Matrix ();

		try {
			m.loadMatrix ();
			m.reduceBandwidth ();
			m.printMatrix ();
		} catch (InvalidMatrixException e) {
			System.err.printf ("Error: %s%n", e.getMessage ());
			System.exit (1);
		}
	}

	private class InvalidMatrixException extends Exception {
		public InvalidMatrixException (String message) {
			super (message);
		}
	}
}
