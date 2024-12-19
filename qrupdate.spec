# For now -- since C code (built with clang) and
# Fortran code (built with gfortran) are linked
# together, LTO object files don't work
%global _disable_lto 1

%define libname		%mklibname %{name}
%define devname		%mklibname %{name} -d
%define oldlibname	%mklibname %{name} 1

# BLAS lib
%global blaslib flexiblas

Summary:	Fortran library for fast updates of QR/Cholesky decompositions
Name:		qrupdate
Version:	1.1.5
Release:	2
License:	GPLv3+
Group:		Development/Other
Url:		https://gitlab.mpi-magdeburg.mpg.de/koehlerm/qrupdate-ng
Source0:	https://gitlab.mpi-magdeburg.mpg.de/koehlerm/qrupdate-ng/-/archive/v%{version}/%{name}-ng-v%{version}.tar.bz2
Source100:	qrupdate.rpmlintrc
BuildRequires:	gcc-gfortran
BuildRequires:	pkgconfig(%{blaslib})

%description
qrupdate is a Fortran library for fast updates of QR and Cholesky
decompositions.

#-----------------------------------------------------------------------

%package -n %{libname}
Summary:	qrupdate shared libraries
Group:		System/Libraries
Obsoletes:	%{oldlibname} < %{EVRD}

%description -n %{libname}
qrupdate is a Fortran library for fast updates of QR and Cholesky
decompositions.

This package contains the shared library required for running programs
built against %{name}.

%files -n %{libname}
%_libdir/*.so.*

#-----------------------------------------------------------------------

%package -n %{devname}
Summary:	qrupdate development files
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
%rename 	%mklibname %{name} -d -s

%description -n %{devname}
qrupdate is a Fortran library for fast updates of QR and Cholesky
decompositions.

This package contains the files required for building programs
that use %{name}.

%files -n %{devname}
%license LICENSE
%doc README.md CHANGELOG
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/*
%{_libdir}/*.so

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-ng-v%{version}

sed -i qrupdate.pc.in \
	-e "s|Requires: blas, lapack|Requires: %{blaslib}|"

%build
export FC=gfortran
%cmake -Wno-dev \
	-DBLA_VENDOR:STRING=FlexiBLAS \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

