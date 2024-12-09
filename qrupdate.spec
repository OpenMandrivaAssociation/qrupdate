%define libname %mklibname %{name}
%define develname %mklibname %{name} -d -s
%define oldlibname %mklibname %{name} 1

# BLAS lib
%global blaslib flexiblas

Summary:	Fortran library for fast updates of QR/Cholesky decompositions
Name:		qrupdate
Version:	1.1.5
Release:	1
License:	GPLv3+
Group:		Development/Other
Url:		https://gitlab.mpi-magdeburg.mpg.de/koehlerm/qrupdate-ng
Source0:	https://gitlab.mpi-magdeburg.mpg.de/koehlerm/qrupdate-ng/-/archive/v%{version}/%{name}-ng-v%{version}.tar.bz2
#Source0:	%{name}-%{version}.tar.gz
Source100:	qrupdate.rpmlintrc
#Patch0:		qrupdate-1.1.1-Makefiles.patch
#Patch1:		qrupdate-enable_debugging.patch
BuildRequires:	gcc-gfortran
BuildRequires:	pkgconfig(%blaslib)

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

%package -n %{develname}
Summary:	qrupdate development files
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
qrupdate is a Fortran library for fast updates of QR and Cholesky
decompositions.

This package contains the files required for building programs
that use %{name}.

%files -n %{develname}
%license LICENSE
%doc README.md CHANGELOG
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/*
%{_libdir}/*.so

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-ng-v%{version}

#sed -i Makeconf \
#	-e "s:LIBDIR=lib:LIBDIR=%{_libdir}:" \
#	-e "/^LIBDIR=/a\PREFIX=/" \
#	-e "s:LAPACK=.*:LAPACK=$(pkg-config --libs lapack):" \
#	-e "s:BLAS=.*:BLAS=$(pkg-config --libs blas):"


%build
#% make_build lib solib
#make_build solib

export FC=gfortran
%cmake -Wno-dev \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

#% ifarch x86_64
#% __sed -i 's,\/lib\/,\/lib64\/,g' src/Makefile
#% endif
#%make_install PREFIX=%{buildroot}/usr
#make_install

