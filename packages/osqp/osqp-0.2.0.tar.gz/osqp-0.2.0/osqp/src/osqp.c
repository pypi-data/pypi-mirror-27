#include "osqp.h"
#include "auxil.h"
#include "util.h"
#include "scaling.h"
#include "glob_opts.h"


#ifndef EMBEDDED
#include "polish.h"
#endif

#ifdef CTRLC
#include "ctrlc.h"
#endif

#ifndef EMBEDDED
#include "lin_sys.h"
#endif

/**********************
 * Main API Functions *
 **********************/


#ifndef EMBEDDED


OSQPWorkspace * osqp_setup(const OSQPData * data, OSQPSettings *settings){
	OSQPWorkspace * work; // Workspace

	// Validate data
	if (validate_data(data)){
#ifdef PRINTING
		c_print("ERROR: Data validation returned failure!\n");
#endif
		return OSQP_NULL;
	}

	// Validate settings
	if (validate_settings(settings)){
#ifdef PRINTING
		c_print("ERROR: Settings validation returned failure!\n");
#endif
		return OSQP_NULL;
	}

	// Allocate empty workspace
	work = c_calloc(1, sizeof(OSQPWorkspace));
	if (!work){
#ifdef PRINTING
		c_print("ERROR: allocating work failure!\n");
#endif
		return OSQP_NULL;
	}

	// Start and allocate directly timer
#ifdef PROFILING
	work->timer = c_malloc(sizeof(OSQPTimer));
	tic(work->timer);
#endif


	// Copy problem data into workspace
	work->data = c_malloc(sizeof(OSQPData));
	work->data->n = data->n;    // Number of variables
	work->data->m = data->m;    // Number of linear constraints
	work->data->P = csc_to_triu(data->P);   // Cost function matrix
	work->data->q = vec_copy(data->q, data->n);    // Linear part of cost function
	work->data->A = copy_csc_mat(data->A);         // Linear constraints matrix
	work->data->l = vec_copy(data->l, data->m);  // Lower bounds on constraints
	work->data->u = vec_copy(data->u, data->m);  // Upper bounds on constraints

	// Vectorized rho parameter
	work->rho_vec     = c_malloc(work->data->m * sizeof(c_float));
	work->rho_inv_vec = c_malloc(work->data->m * sizeof(c_float));

	// Type of constraints
	work->constr_type = c_calloc(work->data->m, sizeof(c_int));

	/*
	 *  Allocate internal solver variables (ADMM steps)
	 */
	work->x = c_calloc(work->data->n, sizeof(c_float));
	work->z = c_calloc(work->data->m, sizeof(c_float));
	work->xz_tilde = c_calloc((work->data->n + work->data->m), sizeof(c_float));
	work->x_prev = c_calloc(work->data->n, sizeof(c_float));
	work->z_prev = c_calloc(work->data->m, sizeof(c_float));
	work->y = c_calloc(work->data->m, sizeof(c_float));

	// Primal and dual residuals variables
	work->Ax = c_calloc(work->data->m, sizeof(c_float));
	work->Px = c_calloc(work->data->n, sizeof(c_float));
	work->Aty = c_calloc(work->data->n, sizeof(c_float));

	// Primal infeasibility variables
	work->delta_y = c_calloc(work->data->m, sizeof(c_float));
	work->Atdelta_y = c_calloc(work->data->n, sizeof(c_float));

	// Dual infeasibility variables
	work->delta_x = c_calloc(work->data->n, sizeof(c_float));
	work->Pdelta_x = c_calloc(work->data->n, sizeof(c_float));
	work->Adelta_x = c_calloc(work->data->m, sizeof(c_float));

	// Copy settings
	work->settings = copy_settings(settings);

	// Perform scaling
	if (settings->scaling) {
		// Allocate scaling structure
		work->scaling = c_malloc(sizeof(OSQPScaling));
		work->scaling->D = c_malloc(work->data->n * sizeof(c_float));
		work->scaling->Dinv = c_malloc(work->data->n * sizeof(c_float));
		work->scaling->E = c_malloc(work->data->m * sizeof(c_float));
		work->scaling->Einv = c_malloc(work->data->m * sizeof(c_float));

		// Allocate workspace variables used in scaling
		work->D_temp = c_malloc(work->data->n * sizeof(c_float));
		work->D_temp_A = c_malloc(work->data->n * sizeof(c_float));
		work->E_temp = c_malloc(work->data->m * sizeof(c_float));

		// Scale data
		scale_data(work);
	}
	else {
		work->scaling = OSQP_NULL;
	}

	// Set type of constraints
	set_rho_vec(work);

	// Load linear system solver
	if ( load_linsys_solver(work->settings->linsys_solver) ) {
#ifdef PRINTING
		c_print("%s linear system solver not available.\nTried to obtain it from shared library.\n",
				LINSYS_SOLVER_NAME[work->settings->linsys_solver]);
#endif
		osqp_cleanup(work);
		return OSQP_NULL;
	}

	// Initialize linear system solver structure
	work->linsys_solver = init_linsys_solver(work->data->P, work->data->A,
			work->settings->sigma, work->rho_vec,
			work->settings->linsys_solver, 0);
	if (!work->linsys_solver) {
#ifdef PRINTING
		c_print("ERROR: Linear systems solver initialization failure!\n");
#endif
		osqp_cleanup(work);
		return OSQP_NULL;
	}


	// Initialize active constraints structure
	work->pol = c_malloc(sizeof(OSQPPolish));
	work->pol->Alow_to_A = c_malloc(work->data->m * sizeof(c_int));
	work->pol->Aupp_to_A = c_malloc(work->data->m * sizeof(c_int));
	work->pol->A_to_Alow = c_malloc(work->data->m * sizeof(c_int));
	work->pol->A_to_Aupp = c_malloc(work->data->m * sizeof(c_int));
	work->pol->x = c_malloc(work->data->n * sizeof(c_float));
	work->pol->z = c_malloc(work->data->m * sizeof(c_float));
	work->pol->y = c_malloc(work->data->m * sizeof(c_float));


	// Allocate solution
	work->solution = c_calloc(1, sizeof(OSQPSolution));
	work->solution->x = c_calloc(1, work->data->n * sizeof(c_float));
	work->solution->y = c_calloc(1, work->data->m * sizeof(c_float));

	// Allocate and initialize information
	work->info = c_calloc(1, sizeof(OSQPInfo));
	work->info->status_polish = 0;  // Polishing not performed
	update_status(work->info, OSQP_UNSOLVED);
#ifdef PROFILING
	work->info->solve_time = 0.0;  // Solve time to zero
	work->info->polish_time = 0.0; // Polish time to zero
	work->info->run_time = 0.0;    // Total run time to zero
	work->info->setup_time = toc(work->timer); // Updater timer information
	work->first_run = 1;
#endif
#if EMBEDDED != 1
	work->info->rho_updates = 0;  // Rho updates set to 0
	work->info->rho_estimate = work->settings->rho;   // Best rho estimate
#endif

	// Print header
#ifdef PRINTING
	if (work->settings->verbose)
		print_setup_header(work);
	work->summary_printed = 0; // Initialize last summary  to not printed
#endif


#if EMBEDDED != 1
        // If adaptive rho and automatic interval, but profiling disabled, we need to
	// set the interval to a default value
#ifndef PROFILING
	if (work->settings->adaptive_rho && !work->settings->adaptive_rho_interval){
		if (work->settings->check_termination){
			// If check_termination is enabled, we set it to a multiple of the check termination interval
			work->settings->adaptive_rho_interval = ADAPTIVE_RHO_MULTIPLE_TERMINATION * work->settings->check_termination;
		} else {
			// If check_termination is disabled we set it to a predefined fix number
			work->settings->adaptive_rho_interval = ADAPTIVE_RHO_FIXED;
		}

	}
#endif
#endif

	// Return workspace structure
	return work;
}

#endif  // #ifndef EMBEDDED




c_int osqp_solve(OSQPWorkspace * work){
	c_int exitflag = 0;
	c_int iter;
	c_int compute_cost_function;  // Boolean whether to compute the cost function
	// in the loop
	c_int can_check_termination = 0;  // Boolean whether to check termination

#ifdef PRINTING
	c_int can_print; // Boolean whether you can print
	compute_cost_function = work->settings->verbose; // Compute cost function only if verbose is on
#else
	compute_cost_function = 0; // Never compute cost function during the iterations if no printing enabled
#endif

	// Check if workspace has been initialized
	if (!work){
#ifdef PRINTING
		c_print("ERROR: Workspace not initialized!\n");
#endif
		return -1;
	}

#ifdef PROFILING
	tic(work->timer); // Start timer
#endif

#ifdef PRINTING
	if (work->settings->verbose){
		// Print Header for every column
		print_header();
	}
#endif

#ifdef CTRLC
	// initialize Ctrl-C support
	startInterruptListener();
#endif

	// Initialize variables (cold start or warm start depending on settings)
	if (!work->settings->warm_start)
		cold_start(work);     // If not warm start -> set z, u to zero

	// Main ADMM algorithm
	for (iter = 1; iter <= work->settings->max_iter; iter ++) {
		// Update x_prev, z_prev (preallocated, no malloc)
		swap_vectors(&(work->x), &(work->x_prev));
		swap_vectors(&(work->z), &(work->z_prev));

		/* ADMM STEPS */
		/* Compute \tilde{x}^{k+1}, \tilde{z}^{k+1} */
		update_xz_tilde(work);

		/* Compute x^{k+1} */
		update_x(work);

		/* Compute z^{k+1} */
		update_z(work);

		/* Compute y^{k+1} */
		update_y(work);

		/* End of ADMM Steps */

#ifdef CTRLC
		// Check the interrupt signal
		if (isInterrupted()) {
			update_status(work->info, OSQP_SIGINT);
			c_print("Solver interrupted\n");
			endInterruptListener();
			return 1;   // exitflag
		}
#endif

		// Can we check for termination ?
		can_check_termination = work->settings->check_termination &&
			(iter % work->settings->check_termination == 0);

#ifdef PRINTING
		// Can we print ?
		can_print = work->settings->verbose &&
			((iter % PRINT_INTERVAL == 0) || (iter == 1));

		if (can_check_termination || can_print){ // Update status in either of these cases
			// Update information
			update_info(work, iter, compute_cost_function, 0);

			if (can_print){
				// Print summary
				print_summary(work);
			}

			if (can_check_termination){
				// Check algorithm termination
				if (check_termination(work, 0)){
					// Terminate algorithm
					break;
				}
			}

		}
#else
		if (can_check_termination){
			// Update information and compute also objective value
			update_info(work, iter, compute_cost_function, 0);

			// Check algorithm termination
			if (check_termination(work, 0)){
				// Terminate algorithm
				break;
			}
		}
#endif


#if EMBEDDED != 1
#ifdef PROFILING
		// If adaptive rho with automatic interval, check if the solve time is a certain fraction 
		// of the setup time.
		if (work->settings->adaptive_rho && !work->settings->adaptive_rho_interval){
			// Check time 
			if (toc(work->timer) > work->settings->adaptive_rho_fraction * work->info->setup_time){
					// Enough time has passed. We round the number of iterations to the
					// closest multiple of check_termination
					work->settings->adaptive_rho_interval = (c_int)c_roundmultiple(iter, work->settings->check_termination);
					// Make sure the interval is not 0 and at least check_termination times
					work->settings->adaptive_rho_interval = c_max(work->settings->adaptive_rho_interval, work->settings->check_termination);
					
// #ifdef PRINTING
//                                         // DEBUG: print stuff
//                                         c_print("time %.2e, iter %i, check_termination %i, new_interval %i\n",
//                                                         toc(work->timer), iter,
//                                                         work->settings->check_termination,
//                                                         work->settings->adaptive_rho_interval);
// #endif
			} // If time condition is met
		}  // If adaptive rho enabled and interval set to auto
#endif // PROFILING
		
		// Adapt rho
		if (work->settings->adaptive_rho &&
				work->settings->adaptive_rho_interval &&	
				(iter % work->settings->adaptive_rho_interval == 0)){
			// Update info with the residuals if it hasn't been done before
#ifdef PRINTING	
			if (!can_check_termination && !can_print){
				// Information has not been computed neither for termination or printing reasons
				update_info(work, iter, compute_cost_function, 0);
			}
#else
			if(!can_check_termination){
				// Information has not been computed before for termination check
				update_info(work, iter, compute_cost_function, 0);
			}
#endif
			
			// Actually update rho
			if(adapt_rho(work)){
#ifdef PRINTING
				c_print("ERROR: Failed rho update!\n");
#endif  // PRINTING
				return 1;
			}

			// This was for debug purposes 
			// #ifdef PRINTING
			//                 if (work->settings->verbose)
			//                         c_print("rho = %.2e\n", work->settings->rho);
			// #endif  // PRINTING

		}
#endif  // EMBEDDED != 1

	}  // End of ADMM for loop

	// Update information and check termination condition if it hasn't been done
	// during last iteration (max_iter reached or check_termination disabled)
	if (!can_check_termination){

		/* Update information */
#ifdef PRINTING
		if(!can_print){
			// Update info only if it hasn't been updated before for printing
			// reasons
			update_info(work, iter-1, compute_cost_function, 0);
		}
#else
		// If no printing is enabled, update info directly
		update_info(work, iter-1, compute_cost_function, 0);
#endif

#ifdef PRINTING
		/* Print summary */
		if (work->settings->verbose && !work->summary_printed)
			print_summary(work);
#endif

		/* Check whether a termination criterion is triggered */
		check_termination(work, 0);
	}

	// Compute objective value in case it was not
	// computed during the iterations
	if (!compute_cost_function){
		work->info->obj_val = compute_obj_val(work, work->x);
	}

	/* Print summary for last iteration */
#ifdef PRINTING
	if (work->settings->verbose && !work->summary_printed){
		print_summary(work);
	}
#endif

	/* if max iterations reached, change status accordingly */
	if (work->info->status_val == OSQP_UNSOLVED) {
		if (!check_termination(work, 1)){ // Try to check for approximate termination
			update_status(work->info, OSQP_MAX_ITER_REACHED);
		}
	}

#if EMBEDDED != 1
        /* Update rho estimate */
        work->info->rho_estimate = compute_rho_estimate(work);
#endif

	/* Update solve time */
#ifdef PROFILING
	work->info->solve_time = toc(work->timer);
#endif

	
	// Polish the obtained solution
#ifndef EMBEDDED
	if (work->settings->polish && work->info->status_val == OSQP_SOLVED)
		polish(work);
#endif

	/* Update total time */
#ifdef PROFILING
	if (work->first_run) {
		// total time: setup + solve + polish
		work->info->run_time = work->info->setup_time +
			work->info->solve_time +
			work->info->polish_time;
	} else {
		// total time: solve + polish
		work->info->run_time = work->info->solve_time +
			work->info->polish_time;
	}
	// Indicate that the solve function has already been executed
	if (work->first_run) work->first_run = 0;
#endif


	/* Print final footer */
#ifdef PRINTING
	if(work->settings->verbose)
		print_footer(work->info, work->settings->polish);
#endif

	// Store solution
	store_solution(work);

	return exitflag;
}


#ifndef EMBEDDED

c_int osqp_cleanup(OSQPWorkspace * work){
	c_int exitflag=0;

	if (work) { // If workspace has been allocated
		// Free Data
		if (work->data) {
			if (work->data->P)        csc_spfree(work->data->P);
			if (work->data->A)        csc_spfree(work->data->A);
			if (work->data->q)        c_free(work->data->q);
			if (work->data->l)        c_free(work->data->l);
			if (work->data->u)        c_free(work->data->u);
			c_free(work->data);
		}

		// Free scaling
		if (work->settings->scaling) {
			if (work->scaling->D)     c_free(work->scaling->D);
			if (work->scaling->Dinv)  c_free(work->scaling->Dinv);
			if (work->scaling->E)     c_free(work->scaling->E);
			if (work->scaling->Einv)  c_free(work->scaling->Einv);
			c_free(work->scaling);

			// Free workspace variables
			if (work->D_temp)         c_free(work->D_temp);
			if (work->D_temp_A)       c_free(work->D_temp_A);
			if (work->E_temp)         c_free(work->E_temp);
		}

		// Free linear system solver structure
		work->linsys_solver->free(work->linsys_solver);

		// Unload linear system solver
		exitflag = unload_linsys_solver(work->settings->linsys_solver);

		// Free active constraints structure
		if (work->pol) {
			if (work->pol->Alow_to_A) c_free(work->pol->Alow_to_A);
			if (work->pol->Aupp_to_A) c_free(work->pol->Aupp_to_A);
			if (work->pol->A_to_Alow) c_free(work->pol->A_to_Alow);
			if (work->pol->A_to_Aupp) c_free(work->pol->A_to_Aupp);
			if (work->pol->x)         c_free(work->pol->x);
			if (work->pol->z)         c_free(work->pol->z);
			if (work->pol->y)         c_free(work->pol->y);
			c_free(work->pol);
		}

		// Free other Variables
		if (work->constr_type)        c_free(work->constr_type);
		if (work->rho_vec)            c_free(work->rho_vec);
		if (work->rho_inv_vec)        c_free(work->rho_inv_vec);
		if (work->x)                  c_free(work->x);
		if (work->z)                  c_free(work->z);
		if (work->xz_tilde)           c_free(work->xz_tilde);
		if (work->x_prev)             c_free(work->x_prev);
		if (work->z_prev)             c_free(work->z_prev);
		if (work->y)                  c_free(work->y);

		if (work->Ax)                 c_free(work->Ax);
		if (work->Px)                 c_free(work->Px);
		if (work->Aty)                c_free(work->Aty);
		if (work->delta_y)            c_free(work->delta_y);
		if (work->Atdelta_y)          c_free(work->Atdelta_y);
		if (work->delta_x)            c_free(work->delta_x);
		if (work->Pdelta_x)           c_free(work->Pdelta_x);
		if (work->Adelta_x)           c_free(work->Adelta_x);

		// Free Settings
		if (work->settings)           c_free(work->settings);

		// Free solution
		if (work->solution) {
			if (work->solution->x)    c_free(work->solution->x);
			if (work->solution->y)    c_free(work->solution->y);
			c_free(work->solution);
		}

		// Free information
		if (work->info)               c_free(work->info);

		// Free timer
#ifdef PROFILING
		if (work->timer)              c_free(work->timer);
#endif

		// Free work
		c_free(work);
	}

	return exitflag;
}

#endif  // #ifndef EMBEDDED


/************************
 * Update problem data  *
 ************************/


c_int osqp_update_lin_cost(OSQPWorkspace * work, c_float * q_new) {

	// Replace q by the new vector
	prea_vec_copy(q_new, work->data->q, work->data->n);

	// Scaling
	if (work->settings->scaling) {
		vec_ew_prod(work->scaling->D, work->data->q, work->data->q, work->data->n);
		vec_mult_scalar(work->data->q, work->scaling->c, work->data->n);
	}

	// Reset solver information
	reset_info(work->info);

	return 0;
}


c_int osqp_update_bounds(OSQPWorkspace * work, c_float * l_new, c_float * u_new) {
	c_int i, exitflag = 0;

	// Check if lower bound is smaller than upper bound
	for (i=0; i<work->data->m; i++) {
		if (l_new[i] > u_new[i]) {
#ifdef PRINTING
			c_print("lower bound must be lower than or equal to upper bound\n");
#endif
			return 1;
		}
	}

	// Replace l and u by the new vectors
	prea_vec_copy(l_new, work->data->l, work->data->m);
	prea_vec_copy(u_new, work->data->u, work->data->m);

	// Scaling
	if (work->settings->scaling) {
		vec_ew_prod(work->scaling->E, work->data->l, work->data->l, work->data->m);
		vec_ew_prod(work->scaling->E, work->data->u, work->data->u, work->data->m);
	}

	// Reset solver information
	reset_info(work->info);

#if EMBEDDED != 1
	// Update rho_vec and refactor if constraints type changes
	exitflag = update_rho_vec(work);
#endif // EMBEDDED != 1

	return exitflag;
}


c_int osqp_update_lower_bound(OSQPWorkspace * work, c_float * l_new) {
	c_int i, exitflag = 0;

	// Replace l by the new vector
	prea_vec_copy(l_new, work->data->l, work->data->m);

	// Scaling
	if (work->settings->scaling) {
		vec_ew_prod(work->scaling->E, work->data->l, work->data->l, work->data->m);
	}

	// Check if lower bound is smaller than upper bound
	for (i=0; i<work->data->m; i++) {
		if (work->data->l[i] > work->data->u[i]) {
#ifdef PRINTING
			c_print("upper bound must be greater than or equal to lower bound\n");
#endif
			return 1;
		}
	}

	// Reset solver information
	reset_info(work->info);

#if EMBEDDED != 1
	// Update rho_vec and refactor if constraints type changes
	exitflag = update_rho_vec(work);
#endif // EMBEDDED ! =1

	return exitflag;
}



c_int osqp_update_upper_bound(OSQPWorkspace * work, c_float * u_new) {
	c_int i, exitflag = 0;

	// Replace u by the new vector
	prea_vec_copy(u_new, work->data->u, work->data->m);

	// Scaling
	if (work->settings->scaling) {
		vec_ew_prod(work->scaling->E, work->data->u, work->data->u, work->data->m);
	}

	// Check if upper bound is greater than lower bound
	for (i=0; i<work->data->m; i++) {
		if (work->data->u[i] < work->data->l[i]) {
#ifdef PRINTING
			c_print("lower bound must be lower than or equal to upper bound\n");
#endif
			return 1;
		}
	}

	// Reset solver information
	reset_info(work->info);

#if EMBEDDED != 1
	// Update rho_vec and refactor if constraints type changes
	exitflag = update_rho_vec(work);
#endif // EMBEDDED != 1

	return exitflag;
}



c_int osqp_warm_start(OSQPWorkspace * work, c_float * x, c_float * y){

	// Update warm_start setting to true
	if (!work->settings->warm_start) work->settings->warm_start = 1;

	// Copy primal and dual variables into the iterates
	prea_vec_copy(x, work->x, work->data->n);
	prea_vec_copy(y, work->y, work->data->m);

	// Scale iterates
	if (work->settings->scaling){
		vec_ew_prod(work->scaling->Dinv, work->x, work->x, work->data->n);
		vec_ew_prod(work->scaling->Einv, work->y, work->y, work->data->m);
		vec_mult_scalar(work->y, work->scaling->c, work->data->m);
	}

	// Compute Ax = z and store it in z
	mat_vec(work->data->A, work->x, work->z, 0);

	return 0;
}


c_int osqp_warm_start_x(OSQPWorkspace * work, c_float * x){

	// Update warm_start setting to true
	if (!work->settings->warm_start) work->settings->warm_start = 1;

	// Copy primal variable into the iterate x
	prea_vec_copy(x, work->x, work->data->n);

	// Scale iterate
	if (work->settings->scaling){
		vec_ew_prod(work->scaling->Dinv, work->x, work->x, work->data->n);
	}

	// Compute Ax = z and store it in z
	mat_vec(work->data->A, work->x, work->z, 0);

	// Cold start y
	vec_set_scalar(work->y, 0., work->data->m);

	return 0;
}



c_int osqp_warm_start_y(OSQPWorkspace * work, c_float * y){

	// Update warm_start setting to true
	if (!work->settings->warm_start) work->settings->warm_start = 1;

	// Copy primal variable into the iterate y
	prea_vec_copy(y, work->y, work->data->m);

	// Scale iterate
	if (work->settings->scaling){
		vec_ew_prod(work->scaling->Einv, work->y, work->y, work->data->m);
		vec_mult_scalar(work->y, work->scaling->c, work->data->m);
	}

	// Cold start x and z
	vec_set_scalar(work->x, 0., work->data->n);
	vec_set_scalar(work->z, 0., work->data->m);

	return 0;
}

#if EMBEDDED != 1
/**
 * Update elements of matrix P (upper-diagonal)
 * without changing sparsity structure.
 *
 *
 *  If Px_new_idx is OSQP_NULL, Px_new is assumed to be as long as P->x
 *  and the whole P->x is replaced.
 *
 * @param  work       Workspace structure
 * @param  Px_new     Vector of new elements in P->x (upper triangular)
 * @param  Px_new_idx Index mapping new elements to positions in P->x
 * @param  P_new_n    Number of new elements to be changed
 * @return            output flag:  0: OK
 *                                  1: P_new_n > nnzP
 *                                 <0: error in update_matrices()
 */
c_int osqp_update_P(OSQPWorkspace * work, c_float * Px_new, c_int * Px_new_idx, c_int P_new_n){
	c_int i; // For indexing
	c_int exitflag; // Exit flag
	c_int nnzP; // Number of nonzeros in P

	nnzP = work->data->P->p[work->data->P->n];

	if (Px_new_idx){ // Passing the index of elements changed
		// Check if number of elements is less or equal than the total number of
		// nonzeros in P
		if (P_new_n > nnzP){
#ifdef PRINTING
			c_print("Error in P update: new number of elements (%i) greater than elements in P (%i)!\n", (int)P_new_n, (int)nnzP);
#endif
			return 1;
		}
	}

	// Unscale data
	unscale_data(work);


	// Update P elements
	if (Px_new_idx){ // Change only Px_new_idx
		for (i = 0; i < P_new_n; i++){
			work->data->P->x[Px_new_idx[i]] = Px_new[i];
		}
	}
	else // Change whole P
	{
		for (i = 0; i < nnzP; i++){
			work->data->P->x[i] = Px_new[i];
		}
	}

	// Scale data
	scale_data(work);

	// Update linear system structure with new data
	exitflag = work->linsys_solver->update_matrices(work->linsys_solver, work->data->P, work->data->A, work->settings);

	// Reset solver information
	reset_info(work->info);

#ifdef PRINTING
	if (exitflag < 0) {
		c_print("Error in P update: new KKT matrix is not quasidefinite!");
	}
#endif

	return exitflag;
}


/**
 * Update elements of matrix A without changing sparsity structure.
 *
 *
 *  If Ax_new_idx is OSQP_NULL, Ax_new is assumed to be as long as A->x
 *  and the whole P->x is replaced.
 *
 * @param  work       Workspace structure
 * @param  Ax_new     Vector of new elements in A->x
 * @param  Ax_new_idx Index mapping new elements to positions in A->x
 * @param  A_new_n    Number of new elements to be changed
 * @return            output flag:  0: OK
 *                                  1: A_new_n > nnzA
 *                                 <0: error in update_matrices()
 */
c_int osqp_update_A(OSQPWorkspace * work, c_float * Ax_new, c_int * Ax_new_idx, c_int A_new_n){
	c_int i; // For indexing
	c_int exitflag; // Exit flag
	c_int nnzA; // Number of nonzeros in A

	nnzA = work->data->A->p[work->data->A->n];

	if (Ax_new_idx){ // Passing the index of elements changed
		// Check if number of elements is less or equal than the total number of
		// nonzeros in A
		if (A_new_n > nnzA){
#ifdef PRINTING
			c_print("Error in A update: new number of elements (%i) greater than elements in A (%i)!\n", (int)A_new_n, (int)nnzA);
#endif
			return 1;
		}
	}

	// Unscale data
	unscale_data(work);

	// Update A elements
	if (Ax_new_idx){ // Change only Ax_new_idx
		for (i = 0; i < A_new_n; i++){
			work->data->A->x[Ax_new_idx[i]] = Ax_new[i];
		}
	}
	else{ // Change whole A
		for (i = 0; i < nnzA; i++){
			work->data->A->x[i] = Ax_new[i];
		}
	}

	// Scale data
	scale_data(work);

	// Update linear system structure with new data
	exitflag = work->linsys_solver->update_matrices(work->linsys_solver, work->data->P, work->data->A, work->settings);

	// Reset solver information
	reset_info(work->info);

#ifdef PRINTING
	if (exitflag < 0) {
		c_print("Error in A update: new KKT matrix is not quasidefinite!");
	}
#endif

	return exitflag;
}



/**
 * Update elements of matrix P (upper-diagonal) and elements of matrix A
 * without changing sparsity structure.
 *
 *
 *  If Px_new_idx is OSQP_NULL, Px_new is assumed to be as long as P->x
 *  and the whole P->x is replaced.
 *
 *  If Ax_new_idx is OSQP_NULL, Ax_new is assumed to be as long as A->x
 *  and the whole P->x is replaced.
 *
 * @param  work       Workspace structure
 * @param  Px_new     Vector of new elements in P->x (upper triangular)
 * @param  Px_new_idx Index mapping new elements to positions in P->x
 * @param  P_new_n    Number of new elements to be changed
 * @param  Ax_new     Vector of new elements in A->x
 * @param  Ax_new_idx Index mapping new elements to positions in A->x
 * @param  A_new_n    Number of new elements to be changed
 * @return            output flag:  0: OK
 *                                  1: P_new_n > nnzP
 *                                  2: A_new_n > nnzA
 *                                 <0: error in update_matrices()
 */
c_int osqp_update_P_A(OSQPWorkspace * work, c_float * Px_new, c_int * Px_new_idx, c_int P_new_n,
		c_float * Ax_new, c_int * Ax_new_idx, c_int A_new_n){
	c_int i; // For indexing
	c_int exitflag; // Exit flag
	c_int nnzP, nnzA; // Number of nonzeros in P and A

	nnzP = work->data->P->p[work->data->P->n];
	nnzA = work->data->A->p[work->data->A->n];


	if (Px_new_idx){ // Passing the index of elements changed
		// Check if number of elements is less or equal than the total number of
		// nonzeros in P
		if (P_new_n > nnzP){
#ifdef PRINTING
			c_print("Error in P update: new number of elements (%i) greater than elements in P (%i)!\n", (int)P_new_n, (int)nnzP);
#endif
			return 1;
		}
	}


	if (Ax_new_idx){ // Passing the index of elements changed
		// Check if number of elements is less or equal than the total number of
		// nonzeros in A
		if (A_new_n > nnzA){
#ifdef PRINTING
			c_print("Error in A update: new number of elements (%i) greater than elements in A (%i)!\n", (int)A_new_n, (int)nnzA);
#endif
			return 2;
		}
	}


	// Unscale data
	unscale_data(work);

	// Update P elements
	if (Px_new_idx){ // Change only Px_new_idx
		for (i = 0; i < P_new_n; i++){
			work->data->P->x[Px_new_idx[i]] = Px_new[i];
		}
	}
	else // Change whole P
	{
		for (i = 0; i < nnzP; i++){
			work->data->P->x[i] = Px_new[i];
		}
	}

	// Update A elements
	if (Ax_new_idx){ // Change only Ax_new_idx
		for (i = 0; i < A_new_n; i++){
			work->data->A->x[Ax_new_idx[i]] = Ax_new[i];
		}
	}
	else{ // Change whole A
		for (i = 0; i < nnzA; i++){
			work->data->A->x[i] = Ax_new[i];
		}
	}


	// Scale data
	scale_data(work);

	// Update linear system structure with new data
	exitflag = work->linsys_solver->update_matrices(work->linsys_solver, work->data->P, work->data->A, work->settings);

	// Reset solver information
	reset_info(work->info);

#ifdef PRINTING
	if (exitflag < 0) {
		c_print("Error in P and A update: new KKT matrix is not quasidefinite!");
	}
#endif

	return exitflag;

}


c_int osqp_update_rho(OSQPWorkspace * work, c_float rho_new){
	c_int exitflag, i;

	// Check value of rho
	if (rho_new <= 0) {
#ifdef PRINTING
		c_print("rho must be positive\n");
#endif
		return 1;
	}

	// Update rho in settings
	work->settings->rho = c_min(c_max(rho_new, RHO_MIN), RHO_MAX);

	// Update rho_vec and rho_inv_vec
	for (i = 0; i < work->data->m; i++){
		if (work->constr_type[i] == 0) {
			// Inequalities
			work->rho_vec[i] = work->settings->rho;
			work->rho_inv_vec[i] = 1. / work->settings->rho;
		}
		else if (work->constr_type[i] == 1){
			// Equalities
			work->rho_vec[i] = RHO_EQ_OVER_RHO_INEQ * work->settings->rho;
			work->rho_inv_vec[i] = 1. / work->rho_vec[i];
		}
	}

	// Update rho_vec in KKT matrix
	exitflag = work->linsys_solver->update_rho_vec(work->linsys_solver,
			work->rho_vec,
			work->data->m);

	return exitflag;
}

#endif // EMBEDDED != 1

/****************************
 * Update problem settings  *
 ****************************/

c_int osqp_update_max_iter(OSQPWorkspace * work, c_int max_iter_new) {
	// Check that max_iter is positive
	if (max_iter_new <= 0) {
#ifdef PRINTING
		c_print("max_iter must be positive\n");
#endif
		return 1;
	}
	// Update max_iter
	work->settings->max_iter = max_iter_new;

	return 0;
}


c_int osqp_update_eps_abs(OSQPWorkspace * work, c_float eps_abs_new) {
	// Check that eps_abs is positive
	if (eps_abs_new <= 0.) {
#ifdef PRINTING
		c_print("eps_abs must be positive\n");
#endif
		return 1;
	}
	// Update eps_abs
	work->settings->eps_abs = eps_abs_new;

	return 0;
}

c_int osqp_update_eps_rel(OSQPWorkspace * work, c_float eps_rel_new) {
	// Check that eps_rel is positive
	if (eps_rel_new <= 0.) {
#ifdef PRINTING
		c_print("eps_rel must be positive\n");
#endif
		return 1;
	}
	// Update eps_rel
	work->settings->eps_rel = eps_rel_new;

	return 0;
}

c_int osqp_update_eps_prim_inf(OSQPWorkspace * work, c_float eps_prim_inf_new){

	// Check that eps_prim_inf is positive
	if (eps_prim_inf_new <= 0.) {
#ifdef PRINTING
		c_print("eps_prim_inf must be positive\n");
#endif
		return 1;
	}
	// Update eps_prim_inf
	work->settings->eps_prim_inf = eps_prim_inf_new;

	return 0;
}



c_int osqp_update_eps_dual_inf(OSQPWorkspace * work, c_float eps_dual_inf_new){

	// Check that eps_dual_inf is positive
	if (eps_dual_inf_new <= 0.) {
#ifdef PRINTING
		c_print("eps_dual_inf must be positive\n");
#endif
		return 1;
	}
	// Update eps_dual_inf
	work->settings->eps_dual_inf = eps_dual_inf_new;


	return 0;
}


c_int osqp_update_alpha(OSQPWorkspace * work, c_float alpha_new) {
	// Check that alpha is between 0 and 2
	if (alpha_new <= 0. || alpha_new >= 2.) {
#ifdef PRINTING
		c_print("alpha must be between 0 and 2\n");
#endif
		return 1;
	}
	// Update alpha
	work->settings->alpha = alpha_new;

	return 0;
}


c_int osqp_update_warm_start(OSQPWorkspace * work, c_int warm_start_new) {
	// Check that warm_start is either 0 or 1
	if (warm_start_new != 0 && warm_start_new != 1) {
#ifdef PRINTING
		c_print("warm_start should be either 0 or 1\n");
#endif
		return 1;
	}
	// Update warm_start
	work->settings->warm_start = warm_start_new;

	return 0;
}


c_int osqp_update_scaled_termination(OSQPWorkspace * work, c_int scaled_termination_new) {
	// Check that scaled_termination is either 0 or 1
	if (scaled_termination_new != 0 && scaled_termination_new != 1) {
#ifdef PRINTING
		c_print("scaled_termination should be either 0 or 1\n");
#endif
		return 1;
	}
	// Update scaled_termination 
	work->settings->scaled_termination = scaled_termination_new;

	return 0;
}

c_int osqp_update_check_termination(OSQPWorkspace * work, c_int check_termination_new) {
	// Check that check_termination is nonnegative
	if (check_termination_new < 0) {
#ifdef PRINTING
		c_print("check_termination should be nonnegative\n");
#endif
		return 1;
	}
	// Update check_termination
	work->settings->check_termination = check_termination_new;

	return 0;
}


#ifndef EMBEDDED

c_int osqp_update_delta(OSQPWorkspace * work, c_float delta_new) {
	// Check that delta is positive
	if (delta_new <= 0.) {
#ifdef PRINTING
		c_print("delta must be positive\n");
#endif
		return 1;
	}
	// Update delta
	work->settings->delta = delta_new;

	return 0;
}

c_int osqp_update_polish(OSQPWorkspace * work, c_int polish_new) {
	// Check that polish is either 0 or 1
	if (polish_new != 0 && polish_new != 1) {
#ifdef PRINTING
		c_print("polish should be either 0 or 1\n");
#endif
		return 1;
	}
	// Update polish
	work->settings->polish = polish_new;

#ifdef PROFILING
	// Reset polish time to zero
	work->info->polish_time = 0.0;
#endif

	return 0;
}


c_int osqp_update_polish_refine_iter(OSQPWorkspace * work, c_int polish_refine_iter_new) {
	// Check that polish_refine_iter is nonnegative
	if (polish_refine_iter_new < 0) {
#ifdef PRINTING
		c_print("polish_refine_iter must be nonnegative\n");
#endif
		return 1;
	}
	// Update polish_refine_iter
	work->settings->polish_refine_iter = polish_refine_iter_new;

	return 0;
}


c_int osqp_update_verbose(OSQPWorkspace * work, c_int verbose_new) {
	// Check that verbose is either 0 or 1
	if (verbose_new != 0 && verbose_new != 1) {
#ifdef PRINTING
		c_print("verbose should be either 0 or 1\n");
#endif
		return 1;
	}
	// Update verbose
	work->settings->verbose = verbose_new;

	return 0;
}


#endif // EMBEDDED
