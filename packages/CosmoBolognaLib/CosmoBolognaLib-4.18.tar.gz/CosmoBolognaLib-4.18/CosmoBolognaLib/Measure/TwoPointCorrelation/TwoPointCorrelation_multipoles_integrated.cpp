/********************************************************************
 *  Copyright (C) 2015 by Federico Marulli and Alfonso Veropalumbo  *
 *  federico.marulli3@unibo.it                                      *
 *                                                                  *
 *  This program is free software; you can redistribute it and/or   * 
 *  modify it under the terms of the GNU General Public License as  *
 *  published by the Free Software Foundation; either version 2 of  *
 *  the License, or (at your option) any later version.             *
 *                                                                  *
 *  This program is distributed in the hope that it will be useful, *
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of  *
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the   *
 *  GNU General Public License for more details.                    *
 *                                                                  *
 *  You should have received a copy of the GNU General Public       *
 *  License along with this program; if not, write to the Free      *
 *  Software Foundation, Inc.,                                      *
 *  59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.       *
 ********************************************************************/

/**
 *  @file
 *  CatalogueAnalysis/TwoPointCorrelation/TwoPointCorrelation_multipoles_integrated.cpp
 *
 *  @brief Methods of the class
 *  TwoPointCorrelation_multipoles_integrated used to measure the
 *  first three multipoles of the two-point correlation function
 *
 *  This file contains the implementation of the methods of the class
 *  TwoPointCorrelation_multipoles_integrated used to measure the
 *  first three multipoles of the two-point correlation function
 *
 *  @authors Federico Marulli, Alfonso Veropalumbo
 *
 *  @authors federico.marulli3@unbo.it, alfonso.veropalumbo@unibo.it
 */


#include "TwoPointCorrelation_multipoles_integrated.h"
#include "Data1D_extra.h"

using namespace cosmobl;
using namespace catalogue;
using namespace chainmesh;
using namespace pairs;
using namespace measure;
using namespace twopt;


// ============================================================================


shared_ptr<data::Data> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::data_with_extra_info (const vector<double> rad, const vector<double> xil, const vector<double> error) const
{
  auto dd2D = cosmobl::measure::twopt::TwoPointCorrelation2D_polar::m_dd;
  
  vector<double> weightTOT(dd2D->nbins_D1(), 0.), scale_mean(dd2D->nbins_D1(), 0.), scale_sigma(dd2D->nbins_D1(), 0.), z_mean(dd2D->nbins_D1(), 0.), z_sigma(dd2D->nbins_D1(), 0.);

  double fact_err, fact_scale, fact_z;
  
  for (int i=0; i<dd2D->nbins_D1(); ++i) {

    for (int j=0; j<dd2D->nbins_D2(); ++j)
      weightTOT[i] += dd2D->PP2D_weighted(i, j);
    
    for (int j=0; j<dd2D->nbins_D2(); ++j) {
      scale_mean[i] += dd2D->scale_D1_mean(i, j)*dd2D->PP2D_weighted(i, j)/weightTOT[i];
      z_mean[i] += dd2D->z_mean(i, j)*dd2D->PP2D_weighted(i, j)/weightTOT[i];
    }

    scale_sigma[i] = pow(dd2D->scale_D1_sigma(i, 0), 2)*dd2D->PP2D_weighted(i, 0);
    z_sigma[i] = pow(dd2D->z_sigma(i, 0), 2)*dd2D->PP2D_weighted(i, 0);
    
    for (int j=1; j<dd2D->nbins_D2(); ++j) {
      if (dd2D->PP2D_weighted(i, j)>0) {
	fact_err = dd2D->PP2D_weighted(i, j)*dd2D->PP2D_weighted(i, j-1)/(dd2D->PP2D_weighted(i, j)+dd2D->PP2D_weighted(i, j-1));
	fact_scale = pow(dd2D->scale_D1_mean(i, j)-dd2D->scale_D1_mean(i, j-1), 2)*fact_err;
	fact_z = pow(dd2D->z_mean(i, j)-dd2D->z_mean(i, j-1), 2)*fact_err;
	scale_sigma[i] += pow(dd2D->scale_D1_sigma(i, j), 2)*dd2D->PP2D_weighted(i, j)+fact_scale;
	z_sigma[i] += pow(dd2D->z_sigma(i, j),2)*weightTOT[i]+fact_z;
      }
    }
  }
  
  vector<vector<double>> extra(4);
  
  for (int i=0; i<dd2D->nbins_D1(); ++i) {
    extra[0].push_back(scale_mean[i]);
    extra[1].push_back(sqrt(scale_sigma[i]/weightTOT[i]));
    extra[2].push_back(z_mean[i]);
    extra[3].push_back(sqrt(z_sigma[i]/weightTOT[i]));
  }
  
  return move(unique_ptr<data::Data1D_extra>(new data::Data1D_extra(rad, xil, error, extra)));
}


// ============================================================================================


vector<double> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::xx () const
{
  vector<double> rad, xx;
  m_dataset->xx(xx);

  for (size_t i=0; i<xx.size()/3; i++)
    rad.push_back(xx[i]);

  return rad;
}


// ============================================================================================


vector<double> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::xiMonopole () const
{
  vector<double> vv; 
  m_dataset->data(vv);

  size_t sz = vv.size();

  vector<double> xi0;
  for (size_t i=0; i<sz/3; i++)
    xi0.push_back(vv[i]);

  return xi0;
}


// ============================================================================================


vector<double> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::errorMonopole () const
{
  vector<double> vv; 
  m_dataset->error(vv);

  size_t sz = vv.size();

  vector<double> error_xi0;

  for (size_t i=0; i<sz/3; i++)
    error_xi0.push_back(vv[i]);

  return error_xi0;
}


// ============================================================================================


vector<double> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::xiQuadrupole () const 
{
  vector<double> vv; 
  m_dataset->data(vv);

  size_t sz = vv.size();

  vector<double> xi2;

  for (size_t i=sz/3; i<2*sz/3; i++)
    xi2.push_back(vv[i]);

  return xi2;
}


// ============================================================================================


vector<double> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::errorQuadrupole () const 
{
  vector<double> vv; 
  m_dataset->error(vv);

  size_t sz = vv.size();

  vector<double> error_xi2;

  for (size_t i=sz/3; i<2*sz/3; i++)
    error_xi2.push_back(vv[i]);

  return error_xi2;
}


// ============================================================================================


vector<double> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::xiHexadecapole () const
{
  vector<double> vv; 
  m_dataset->data(vv);

  size_t sz = vv.size();

  vector<double> xi4;

  for (size_t i=2*sz/3; i<sz; i++)
    xi4.push_back(vv[i]);

  return xi4;
}


// ============================================================================================


vector<double> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::errorHexadecapole () const 
{
  vector<double> vv; 
  m_dataset->error(vv);

  size_t sz = vv.size();

  vector<double> error_xi4;
  
  for (size_t i=2*sz/3; i<sz; i++)
    error_xi4.push_back(vv[i]);

  return error_xi4;
}


// ============================================================================================


shared_ptr<data::Data> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::Multipoles (const vector<double> rr, const vector<double> mu, const vector<vector<double>> xi, const vector<vector<double>> error_xi)
{
  vector<double> rad, xil, error;

  rad.resize(rr.size()*3);
  xil.resize(0); xil.resize(rr.size()*3, 0.);
  error.resize(0); error.resize(rr.size()*3, 0.);

  double binSize = mu[1]-mu[0];

  for (size_t i=0; i<rr.size(); i++) {

    rad[i] = rr[i];
    rad[i+rr.size()] = rr[i];
    rad[i+2*rr.size()] = rr[i];


    for (size_t j=0; j<mu.size(); j++) {
      double mmu = mu[j];
      double _xibinSize = xi[i][j]*binSize;
      double _exibinSize = error_xi[i][j]*binSize;

      xil[i]             += _xibinSize;             // xi_0
      xil[i+rr.size()]   += 5.*P_2(mmu)*_xibinSize; // xi_2
      xil[i+2*rr.size()] += 9.*P_4(mmu)*_xibinSize; // xi_4

      error[i]           += pow(_exibinSize, 2);               // error[xi_0]
      error[i+rr.size()] += pow(5.*P_2(mmu)*_exibinSize, 2);   // error[xi_2]
      error[i+2*rr.size()] += pow(9.*P_4(mmu)*_exibinSize, 2); // error[xi_4]
    } 

    error[i] = sqrt(error[i]);
    error[i+rr.size()] = sqrt(error[i]);
    error[i+2*rr.size()] = sqrt(error[i]);

  } 
  
  return (!m_compute_extra_info) ? move(unique_ptr<data::Data1D>(new data::Data1D(rad, xil, error))) : data_with_extra_info(rad, xil, error);
}


// ============================================================================================


void cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::measure (const ErrorType errorType, const string dir_output_pairs, const vector<string> dir_input_pairs, const string dir_output_resample, const int nMocks, const bool count_dd, const bool count_rr, const bool count_dr, const bool tcount, const Estimator estimator, const int seed)
{
  switch (errorType) {
    case (ErrorType::_Poisson_) :
      measurePoisson(dir_output_pairs, dir_input_pairs, count_dd, count_rr, count_dr, tcount, estimator);
      break;
    case (ErrorType::_Jackknife_) :
      measureJackknife(dir_output_pairs, dir_input_pairs, dir_output_resample, count_dd, count_rr, count_dr, tcount, estimator);
      break;
    case (ErrorType::_Bootstrap_) :
      measureBootstrap(nMocks, dir_output_pairs, dir_input_pairs, dir_output_resample, count_dd, count_rr, count_dr, tcount, estimator, seed);
      break;
    default:
      ErrorCBL("Error in measure() of TwoPointCorrelation_multipoles_integrated.cpp, unknown type of error");
  }
}


// ============================================================================================


void cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::measurePoisson (const string dir_output_pairs, const vector<string> dir_input_pairs, const bool count_dd, const bool count_rr, const bool count_dr, const bool tcount, const Estimator estimator)
{
  // ----------- measure the 2D two-point correlation function, xi(r, mu) ----------- 

  TwoPointCorrelation2D_polar::measurePoisson(dir_output_pairs, dir_input_pairs, count_dd, count_rr, count_dr, tcount, estimator);

  
  // ----------- integrate the 2D two-point correlation function over the angle mu ----------- 
  
  m_dataset = Multipoles(TwoPointCorrelation2D_polar::xx(), TwoPointCorrelation2D_polar::yy(), TwoPointCorrelation2D_polar::xi2D(), TwoPointCorrelation2D_polar::error2D());
}


// ============================================================================================


void cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::measureJackknife (const string dir_output_pairs, const vector<string> dir_input_pairs, const string dir_output_resample, const bool count_dd, const bool count_rr, const bool count_dr, const bool tcount, const Estimator estimator)
{
  if (dir_output_resample != par::defaultString) {
    string mkdir = "mkdir -p "+dir_output_resample;
    if (system(mkdir.c_str())) {}
  }

  vector<shared_ptr<data::Data>> data;
  vector<shared_ptr<pairs::Pair>> dd_regions, rr_regions, dr_regions;
  count_allPairs_region(dd_regions, rr_regions, dr_regions, TwoPType::_2D_polar_, dir_output_pairs, dir_input_pairs, count_dd, count_rr, count_dr, tcount, estimator);

  auto data_polar = (estimator==_natural_) ? correlation_NaturalEstimator(m_dd, m_rr) : correlation_LandySzalayEstimator(m_dd, m_rr, m_dr);

  if (estimator==_natural_) 
    data = XiJackknife(dd_regions, rr_regions);
  else if (estimator==_LandySzalay_)
    data = XiJackknife(dd_regions, rr_regions, dr_regions);
  else
    ErrorCBL("Error in measurJackknife() of TwoPointCorrelation_multipoles_integrated.cpp: the chosen estimator is not implemented!");
  
  vector<vector<double>> ww, covariance;
  for (size_t i=0; i<data.size(); i++) {
    ww.push_back(data[i]->data());
    
    if (dir_output_resample != par::defaultString) {
      string file_out = dir_output_resample+"xi_multipoles_Jackknife_"+conv(i,par::fINT)+".dat";

      vector<double> rad; data[i]->xx(rad);
      vector<double> xil = data[i]->data();
      vector<double> error = data[i]->error();

      checkDim(rad, m_dd->nbins_D1()*3, "rad");

      ofstream fout(file_out.c_str()); checkIO(fout, file_out);

      fout << "### [1] separation at the bin centre # [2] monopole # [3] error on the monopole # [4] quadrupole # [5] error on the quadrupole # [6] hexadecapole # [7] error on the hexadecapole ###" << endl;

      for (int i=0; i<m_dd->nbins_D1(); i++) 
	fout << setiosflags(ios::fixed) << setprecision(5) << setw(8) << rad[i] << "  " << setw(8) << xil[i] << "  " << setw(8) << error[i] << "  " << setw(8) << xil[i+m_dd->nbins_D1()] << "  " << setw(8) << error[i+m_dd->nbins_D1()] << "  " << setw(8) << xil[i+2*m_dd->nbins_D1()] << "  " << setw(8) << error[i+2*m_dd->nbins_D1()] << endl;

      fout.close(); cout << endl; coutCBL << "I wrote the file: " << file_out << endl << endl;

    }
  }

  covariance_matrix(ww, covariance, 1);

  vector<double> xx_polar, yy_polar;
  vector<vector<double>> dd_polar, error_polar;
  data_polar->xx(xx_polar); data_polar->yy(yy_polar);
  data_polar->data(dd_polar); data_polar->error(error_polar);

  m_dataset = Multipoles(xx_polar, yy_polar, dd_polar, error_polar);
  m_dataset->set_covariance(covariance);
}


// ============================================================================================


void cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::measureBootstrap (const int nMocks, const string dir_output_pairs, const vector<string> dir_input_pairs, const string dir_output_resample, const bool count_dd, const bool count_rr, const bool count_dr, const bool tcount, const Estimator estimator, const int seed)
{
  if (dir_output_resample != par::defaultString) {
    string mkdir = "mkdir -p "+dir_output_resample;
    if (system(mkdir.c_str())) {}
  }
  
  vector<shared_ptr<data::Data>> data;
  vector<shared_ptr<pairs::Pair>> dd_regions, rr_regions, dr_regions;
  count_allPairs_region(dd_regions, rr_regions, dr_regions, TwoPType::_2D_polar_, dir_output_pairs, dir_input_pairs, count_dd, count_rr, count_dr, tcount, estimator);

  auto data_polar = (estimator==_natural_) ? correlation_NaturalEstimator(m_dd, m_rr) : correlation_LandySzalayEstimator(m_dd, m_rr, m_dr);

  if (estimator==_natural_) 
    data = XiBootstrap(nMocks, dd_regions, rr_regions, seed);
  else if (estimator==_LandySzalay_)
    data = XiBootstrap(nMocks, dd_regions, rr_regions, dr_regions, seed);
  else
    ErrorCBL("Error in measureBootstrap() of TwoPointCorrelation_multipoles_integrated.cpp: the chosen estimator is not implemented!");
  
  vector<vector<double>> ww, covariance;
  for (size_t i=0; i<data.size(); i++) {
    ww.push_back(data[i]->data());
    
    if (dir_output_resample != par::defaultString) {
      string file_out = dir_output_resample+"xi_multipoles_Bootstrap_"+conv(i,par::fINT)+".dat";

      vector<double> rad; data[i]->xx(rad);
      vector<double> xil = data[i]->data();
      vector<double> error = data[i]->error();

      checkDim(rad, m_dd->nbins_D1()*3, "rad");

      ofstream fout(file_out.c_str()); checkIO(fout, file_out);

      fout << "### [1] separation at the bin centre # [2] monopole # [3] error on the monopole # [4] quadrupole # [5] error on the quadrupole # [6] hexadecapole # [7] error on the hexadecapole ###" << endl;

      for (int i=0; i<m_dd->nbins_D1(); i++) 
	fout << setiosflags(ios::fixed) << setprecision(5) << setw(8) << rad[i] << "  " << setw(8) << xil[i] << "  " << setw(8) << error[i] << "  " << setw(8) << xil[i+m_dd->nbins_D1()] << "  " << setw(8) << error[i+m_dd->nbins_D1()] << "  " << setw(8) << xil[i+2*m_dd->nbins_D1()] << "  " << setw(8) << error[i+2*m_dd->nbins_D1()] << endl;

      fout.close(); cout << endl; coutCBL << "I wrote the file: " << file_out << endl << endl;

    }
  }
  
  covariance_matrix(ww, covariance, 0);

  vector<double> xx_polar, yy_polar;
  vector<vector<double>> dd_polar, error_polar;
  data_polar->xx(xx_polar); data_polar->yy(yy_polar);
  data_polar->data(dd_polar); data_polar->error(error_polar);

  m_dataset = Multipoles(xx_polar, yy_polar, dd_polar, error_polar);
  m_dataset->set_covariance(covariance);
}


// ============================================================================================


vector<shared_ptr<data::Data>> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::XiJackknife (const vector<shared_ptr<pairs::Pair>> dd, const vector<shared_ptr<pairs::Pair>> rr)
{
  vector<shared_ptr<data::Data>> data;
  auto data2d = TwoPointCorrelation2D_polar::XiJackknife(dd, rr);

  for (size_t i=0; i<data2d.size(); i++){
    vector<double> xx_polar, yy_polar;
    vector<vector<double>> dd_polar, error_polar;
    data2d[i]->xx(xx_polar); data2d[i]->yy(yy_polar);
    data2d[i]->data(dd_polar); data2d[i]->error(error_polar);
    data.push_back(move(Multipoles(xx_polar, yy_polar, dd_polar, error_polar)));
  }
  
  return data;
}


// ============================================================================================


vector<shared_ptr<data::Data>> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::XiJackknife (const vector<shared_ptr<pairs::Pair>> dd, const vector<shared_ptr<pairs::Pair>> rr, const vector<shared_ptr<pairs::Pair>> dr)
{
  vector<shared_ptr<data::Data>> data;
  auto data2d = TwoPointCorrelation2D_polar::XiJackknife(dd, rr, dr);

  for (size_t i=0; i<data2d.size(); i++){
    vector<double> xx_polar, yy_polar;
    vector<vector<double>> dd_polar, error_polar;
    data2d[i]->xx(xx_polar); data2d[i]->yy(yy_polar);
    data2d[i]->data(dd_polar); data2d[i]->error(error_polar);
    data.push_back(move(Multipoles(xx_polar, yy_polar, dd_polar, error_polar)));
  }
  
  return data;
}


// ============================================================================================


vector<shared_ptr<data::Data>> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::XiBootstrap (const int nMocks, const vector<shared_ptr<pairs::Pair>> dd, const vector<shared_ptr<pairs::Pair>> rr, const int seed)
{
  vector<shared_ptr<data::Data>> data;
  auto data2d = TwoPointCorrelation2D_polar::XiBootstrap(nMocks, dd, rr, seed);

  for (size_t i=0; i<data2d.size(); i++){
    vector<double> xx_polar, yy_polar;
    vector<vector<double>> dd_polar, error_polar;
    data2d[i]->xx(xx_polar); data2d[i]->yy(yy_polar);
    data2d[i]->data(dd_polar); data2d[i]->error(error_polar);
    data.push_back(move(Multipoles(xx_polar, yy_polar, dd_polar, error_polar)));
  }

  return data;
}

// ============================================================================================


vector<shared_ptr<data::Data>> cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::XiBootstrap (const int nMocks, const vector<shared_ptr<pairs::Pair>> dd, const vector<shared_ptr<pairs::Pair>> rr, const vector<shared_ptr<pairs::Pair>> dr, const int seed)
{
  vector<shared_ptr<data::Data>> data;
  auto data2d = TwoPointCorrelation2D_polar::XiBootstrap(nMocks, dd, rr, dr, seed);

  for (size_t i=0; i<data2d.size(); i++) {
    vector<double> xx_polar, yy_polar;
    vector<vector<double>> dd_polar, error_polar;
    data2d[i]->xx(xx_polar); data2d[i]->yy(yy_polar);
    data2d[i]->data(dd_polar); data2d[i]->error(error_polar);
    data.push_back(move(Multipoles(xx_polar, yy_polar, dd_polar, error_polar)));
  }
  
  return data;
}


// ============================================================================================


void cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::write (const string dir, const string file, const int rank) const 
{
  (void)rank;
  
  vector<double> rad; m_dataset->xx(rad);
  vector<double> xil = m_dataset->data();
  vector<double> error = m_dataset->error();

  checkDim(rad, m_dd->nbins_D1()*3, "rad");
  
  string file_out = dir+file;
  ofstream fout(file_out.c_str()); checkIO(fout, file_out);

  string header = "[1] separation at the bin centre # [2] monopole # [3] error on the monopole # [4] quadrupole # [5] error on the quadrupole # [6] hexadecapole # [7] error on the hexadecapole";
  
  if (m_compute_extra_info) header += " # [8] mean separation # [9] standard deviation of the separation distribution # [10] mean redshift # [11] standard deviation of the redshift distribution";
  
  fout << "### " << header << " ###" <<endl;

  for (int i=0; i<m_dd->nbins_D1(); i++) {
    fout << setiosflags(ios::fixed) << setprecision(5) << setw(8) << rad[i] << "  " << setw(8) << xil[i] << "  " << setw(8) << error[i] << "  " << setw(8) << xil[i+m_dd->nbins_D1()] << "  " << setw(8) << error[i+m_dd->nbins_D1()] << "  " << setw(8) << xil[i+2*m_dd->nbins_D1()] << "  " << setw(8) << error[i+2*m_dd->nbins_D1()];
    if (m_compute_extra_info)
      for (size_t ex=0; ex<m_dataset->extra_info().size(); ++ex)
	fout << "   " << setw(8) << m_dataset->extra_info(ex, i);
    fout << endl;
  }
   
  fout.close(); cout << endl; coutCBL << "I wrote the file: " << file_out << endl << endl;
}


// ============================================================================


void cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::read_covariance (const string dir, const string file)
{
  m_dataset->set_covariance(dir+file);
}


// ============================================================================


void cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::write_covariance (const string dir, const string file) const
{
  m_dataset->write_covariance(dir, file);
}


// ============================================================================


void cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::compute_covariance (const vector<shared_ptr<data::Data>> xi, const bool JK)
{
  vector<vector<double>> Xi;

  for (size_t i=0; i<xi.size(); i++)
    Xi.push_back(xi[i]->data());

  vector<vector<double>> cov_mat;
  cosmobl::covariance_matrix(Xi, cov_mat, JK);
  
  m_dataset->set_covariance(cov_mat);
}


// ============================================================================


void cosmobl::measure::twopt::TwoPointCorrelation_multipoles_integrated::compute_covariance (const vector<string> file, const bool JK)
{
  vector<double> rad, mean;
  vector<vector<double>> cov_mat;

  cosmobl::covariance_matrix (file, rad, mean, cov_mat, JK); 
  m_dataset->set_covariance(cov_mat);
}
