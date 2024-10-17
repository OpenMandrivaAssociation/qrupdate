%define major	1

%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d -s

Summary:	Fortran library for fast updates of QR/Cholesky decompositions
Name:		qrupdate
Version:	1.1.2
Release:	5
License:	GPLv3+
Group:		Development/Other
Url:		https://qrupdate.sourceforge.net/
Source0:	%{name}-%{version}.tar.gz
Source100:	qrupdate.rpmlintrc
Patch0:		qrupdate-1.1.1-Makefiles.patch
Patch1:		qrupdate-enable_debugging.patch
BuildRequires:	gcc-gfortran
BuildRequires:	blas-devel
BuildRequires:	lapack-devel

%description
qrupdate is a Fortran library for fast updates of QR and Cholesky
decompositions.

%package -n %{libname}
Summary:	qrupdate shared libraries
Group:		System/Libraries

%description -n %{libname}
qrupdate is a Fortran library for fast updates of QR and Cholesky
decompositions.

This package contains the shared library required for running programs
built against %{name}.

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

%prep
%setup -q
%autopatch -p1

sed -i Makeconf \
	-e "s:LIBDIR=lib:LIBDIR=%{_libdir}:" \
	-e "/^LIBDIR=/a\PREFIX=/" \
	-e "s:LAPACK=.*:LAPACK=$(pkg-config --libs lapack):" \
	-e "s:BLAS=.*:BLAS=$(pkg-config --libs blas):"


%build
#% make_build lib solib
%make_build solib

%install

#% ifarch x86_64
#% __sed -i 's,\/lib\/,\/lib64\/,g' src/Makefile
#% endif
#%make_install PREFIX=%{buildroot}/usr
%make_install

%files -n %{libname}
%_libdir/*.so.*

%files -n %{develname}
%doc README ChangeLog COPYING
%{_libdir}/*.so
%{_libdir}/*.a


%changelog
* Sat Apr 28 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.1.2-1mdv2012.0
+ Revision: 794251
- version update 1.1.2

  + Stéphane Téletchéa <steletch@mandriva.org>
    - update to new version 1.1.1

* Thu Jun 11 2009 Lev Givon <lev@mandriva.org> 1.0.1-2mdv2010.0
+ Revision: 385211
- Force rebuild.
- imported package qrupdate

